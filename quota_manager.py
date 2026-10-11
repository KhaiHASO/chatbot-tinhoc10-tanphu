# -*- coding: utf-8 -*-
"""
Bộ quản lý hạn ngạch và chi phí bảo vệ ngân sách ($0.20).
Lưu trữ trạng thái vào SQLite để không bao giờ bị reset khi server khởi động lại.
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "usage.db")

# Ngưỡng an toàn bảo vệ ngân sách của anh Khải
DEFAULT_HARD_LIMIT_USD = 0.18  # Dừng ngay trước khi chạm mốc 0.20 đô
DEFAULT_MAX_REQUESTS = 200     # Tối đa 200 câu hỏi cho cả dự án

# Giá DeepSeek V3 (USD trên 1M tokens) - tính theo mức thận trọng cao nhất
PRICE_INPUT_PER_1M = 0.27      # 0.27$ / 1,000,000 prompt tokens
PRICE_OUTPUT_PER_1M = 1.10     # 1.10$ / 1,000,000 completion tokens

class QuotaManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usage_stats (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    total_requests INTEGER DEFAULT 0,
                    total_prompt_tokens INTEGER DEFAULT 0,
                    total_completion_tokens INTEGER DEFAULT 0,
                    total_cost_usd REAL DEFAULT 0.0,
                    hard_limit_usd REAL DEFAULT 0.18,
                    max_requests INTEGER DEFAULT 200
                )
            """)
            cursor.execute("SELECT COUNT(*) FROM usage_stats WHERE id = 1")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO usage_stats (id, total_requests, total_prompt_tokens, total_completion_tokens, total_cost_usd, hard_limit_usd, max_requests)
                    VALUES (1, 0, 0, 0, 0.0, ?, ?)
                """, (DEFAULT_HARD_LIMIT_USD, DEFAULT_MAX_REQUESTS))
            conn.commit()

    def can_proceed(self) -> tuple[bool, str]:
        """Kiểm tra xem hệ thống còn trong hạn ngạch an toàn không."""
        stats = self.get_stats()
        
        # 1. Kiểm tra ngân sách tiền đô
        if stats["total_cost_usd"] >= stats["hard_limit_usd"]:
            return False, f"⚠️ Đã kích hoạt chốt ngắt an toàn ngân sách! Dự án đã sử dụng ${stats['total_cost_usd']:.4f} / ${stats['hard_limit_usd']:.2f}. API tạm dừng để bảo vệ tài khoản của bạn."
            
        # 2. Kiểm tra tổng số lượt hỏi
        if stats["total_requests"] >= stats["max_requests"]:
            return False, f"⚠️ Đã hoàn thành định mức {stats['max_requests']} câu hỏi thử nghiệm của lớp 10A11! Vui lòng liên hệ quản trị viên để mở thêm."
            
        return True, ""

    def record_usage(self, prompt_tokens: int, completion_tokens: int):
        """Ghi nhận token thực tế trả về từ DeepSeek và tính toán chi phí chính xác."""
        call_cost = (prompt_tokens / 1_000_000 * PRICE_INPUT_PER_1M) + (completion_tokens / 1_000_000 * PRICE_OUTPUT_PER_1M)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usage_stats
                SET total_requests = total_requests + 1,
                    total_prompt_tokens = total_prompt_tokens + ?,
                    total_completion_tokens = total_completion_tokens + ?,
                    total_cost_usd = total_cost_usd + ?
                WHERE id = 1
            """, (prompt_tokens, completion_tokens, call_cost))
            conn.commit()
            
        return call_cost

    def get_stats(self) -> dict:
        """Lấy thông số thống kê thời gian thực."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT total_requests, total_prompt_tokens, total_completion_tokens, total_cost_usd, hard_limit_usd, max_requests FROM usage_stats WHERE id = 1")
            row = cursor.fetchone()
            if row:
                total_req, p_tokens, c_tokens, cost, limit_usd, max_req = row
                pct_cost = min(100.0, (cost / limit_usd * 100)) if limit_usd > 0 else 100.0
                pct_req = min(100.0, (total_req / max_req * 100)) if max_req > 0 else 100.0
                return {
                    "total_requests": total_req,
                    "max_requests": max_req,
                    "total_prompt_tokens": p_tokens,
                    "total_completion_tokens": c_tokens,
                    "total_cost_usd": cost,
                    "hard_limit_usd": limit_usd,
                    "pct_cost": pct_cost,
                    "pct_req": pct_req,
                    "remaining_requests": max(0, max_req - total_req),
                    "remaining_budget": max(0.0, limit_usd - cost)
                }
            return {
                "total_requests": 0, "max_requests": DEFAULT_MAX_REQUESTS,
                "total_cost_usd": 0.0, "hard_limit_usd": DEFAULT_HARD_LIMIT_USD,
                "pct_cost": 0.0, "pct_req": 0.0,
                "remaining_requests": DEFAULT_MAX_REQUESTS,
                "remaining_budget": DEFAULT_HARD_LIMIT_USD
            }

    def reset_quota_for_test(self):
        """Dùng cho quản trị viên reset lại hạn ngạch nếu muốn."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE usage_stats SET total_requests = 0, total_prompt_tokens = 0, total_completion_tokens = 0, total_cost_usd = 0.0 WHERE id = 1")
            conn.commit()

quota_mgr = QuotaManager()
