# -*- coding: utf-8 -*-
"""
Module tìm kiếm và trích xuất ngữ cảnh kiến thức từ SGK Tin học 10 (KNTT).
Tối ưu hóa token để bảo vệ ngân sách ($0.20) cho dự án.
"""

import os
import json
import re

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "tin10_knowledge.json")

class KnowledgeBase:
    def __init__(self, data_file=DATA_PATH):
        self.lessons = []
        if os.path.exists(data_file):
            with open(data_file, "r", encoding="utf-8") as f:
                self.lessons = json.load(f)
        self.lesson_map = {f"B{l['lesson_num']}": l for l in self.lessons}
        self.lesson_num_map = {l['lesson_num']: l for l in self.lessons}

    def get_all_lessons(self):
        """Trả về danh sách tóm tắt tất cả các bài để hiển thị trên UI."""
        return [
            {
                "id": l["id"],
                "lesson_num": l["lesson_num"],
                "title": l["title"],
                "topic": l["topic"],
                "total_slides": l.get("total_slides", 0)
            }
            for l in self.lessons
        ]

    def get_lesson_by_num(self, num):
        return self.lesson_num_map.get(num)

    def search_relevant_context(self, query: str, top_k: int = 1, max_chars: int = 2500) -> str:
        """
        Tìm kiếm bài học liên quan nhất dựa trên truy vấn của học sinh.
        Chỉ trích xuất tối đa max_chars (~500 - 700 tokens) để tiết kiệm chi phí DeepSeek.
        """
        query_lower = query.lower()
        
        # 1. Kiểm tra xem học sinh có nhắc đích danh bài số mấy không (vd: "bài 20", "bài 4")
        match = re.search(r"bài\s*(\d+)", query_lower)
        if match:
            num = int(match.group(1))
            if num in self.lesson_num_map:
                lesson = self.lesson_num_map[num]
                snippet = self._extract_snippet(lesson, query_lower, max_chars)
                return f"【TÀI LIỆU SGK: {lesson['title']} - {lesson['topic']}】\n{snippet}"

        # 2. Tính điểm số khớp từ khóa theo bài
        scores = []
        # Tách từ khóa (loại bỏ từ vô nghĩa ngắn)
        words = [w for w in re.findall(r"[\w\d]+", query_lower) if len(w) > 1]
        
        for lesson in self.lessons:
            score = 0
            title_lower = lesson["title"].lower()
            topic_lower = lesson["topic"].lower()
            content_lower = lesson["content"].lower()
            
            for w in words:
                # Trọng số tiêu đề cực cao
                if w in title_lower:
                    score += 15
                elif w in topic_lower:
                    score += 5
                
                # Đếm tần suất trong nội dung
                count = content_lower.count(w)
                score += min(count, 5) # cap để không bị thiên vị bài dài
            
            scores.append((score, lesson))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # Lấy top kết quả nếu score > 0
        best_matches = [item for item in scores if item[0] > 0][:top_k]
        
        if not best_matches:
            return ""
        
        contexts = []
        for score, lesson in best_matches:
            snippet = self._extract_snippet(lesson, query_lower, max_chars)
            contexts.append(f"【TÀI LIỆU SGK: {lesson['title']} - {lesson['topic']}】\n{snippet}")
            
        return "\n\n".join(contexts)

    def _extract_snippet(self, lesson: dict, query_lower: str, max_chars: int) -> str:
        """Trích xuất các slide có liên quan nhất trong bài học."""
        content = lesson.get("content", "")
        slides = content.split("[Slide ")
        
        if len(content) <= max_chars:
            return content
            
        words = [w for w in re.findall(r"[\w\d]+", query_lower) if len(w) > 2]
        scored_slides = []
        
        for slide in slides:
            if not slide.strip():
                continue
            slide_lower = slide.lower()
            sc = sum(slide_lower.count(w) for w in words)
            # Ưu tiên các slide chứa định nghĩa, cú pháp
            if any(k in slide_lower for k in ["cú pháp", "ví dụ", "khái niệm", "lưu ý", "chú ý"]):
                sc += 2
            scored_slides.append((sc, slide))
            
        scored_slides.sort(key=lambda x: x[0], reverse=True)
        
        selected_text = []
        current_len = 0
        for sc, slide in scored_slides:
            slide_text = f"[Slide {slide.strip()}"
            if current_len + len(slide_text) > max_chars:
                break
            selected_text.append(slide_text)
            current_len += len(slide_text)
            
        if not selected_text:
            return content[:max_chars] + "\n...(tóm lược tài liệu)"
            
        return "\n\n".join(selected_text)

# Khởi tạo singleton
kb = KnowledgeBase()
