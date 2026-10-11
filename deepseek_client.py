# -*- coding: utf-8 -*-
"""
Module kết nối DeepSeek API có hỗ trợ Streaming, Token Tracking và Guardrail.
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

SYSTEM_INSTRUCTION = """Bạn là "Trợ lý AI Tin học 10" - một trợ lý học tập thông minh và thân thiện, được phát triển bởi hai học sinh Phan Trọng Hiếu và Phạm Mạnh Long (Lớp 10A11, Trường THPT Tân Phú).

Nhiệm vụ của bạn:
1. Hỗ trợ học sinh và thầy cô giải đáp các thắc mắc về môn Tin học lớp 10 theo đúng chuẩn sách giáo khoa "Kết nối tri thức với cuộc sống" (KNTT).
2. Khi giải thích lý thuyết: Trình bày mạch lạc, dễ hiểu, gạch đầu dòng rõ ràng, chuẩn thuật ngữ SGK.
3. Khi hướng dẫn lập trình Python: Cung cấp đoạn code mẫu chuẩn xác, có chú thích (comment) rõ ràng, giải thích từng dòng lệnh và lưu ý các lỗi thường gặp (như thụt lề IndentationError, sai kiểu dữ liệu TypeError, v.v.).
4. Khi hướng dẫn đồ họa Inkscape hoặc phần cứng/mạng: Hướng dẫn các bước thao tác thực hành cụ thể.
5. Luôn giữ phong cách sư phạm, lịch sự, khuyến khích tinh thần tự học của các bạn học sinh.
6. Nếu câu hỏi hoàn toàn không liên quan đến môn Tin học lớp 10 (ví dụ: hỏi chuyện phiếm, lịch sử, game không liên quan...), hãy lịch sự từ chối và nhắc nhở học sinh quay lại chủ đề môn Tin học 10.
"""

def get_api_key():
    """Lấy API key từ env hoặc Streamlit secrets."""
    # 1. Thử lấy từ st.secrets nếu đang chạy Streamlit
    try:
        import streamlit as st
        if "DEEPSEEK_API_KEY" in st.secrets:
            return st.secrets["DEEPSEEK_API_KEY"]
    except Exception:
        pass
    
    # 2. Lấy từ biến môi trường
    return os.getenv("DEEPSEEK_API_KEY", "")

def generate_chat_stream(messages: list, context: str = "", max_tokens: int = 650):
    """
    Gửi tin nhắn đến DeepSeek API và stream kết quả về cho giao diện.
    Trả về generator sinh ra các đoạn văn bản (text delta) và cuối cùng yield usage dict.
    """
    api_key = get_api_key()
    if not api_key:
        yield "LỖI: Chưa cấu hình DEEPSEEK_API_KEY trong hệ thống!"
        return

    # Chuẩn bị system prompt có đính kèm ngữ cảnh trích xuất từ SGK
    system_prompt = SYSTEM_INSTRUCTION
    if context:
        system_prompt += f"\n\n--- DỮ LIỆU THAM KHẢO TỪ SGK TIN 10 KNTT ---\n{context}\n------------------------------------------\nHãy ưu tiên đối chiếu tài liệu trên để trả lời thật sát bài học."

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    payload = {
        "model": "deepseek-chat",
        "messages": full_messages,
        "temperature": 0.5,
        "max_tokens": max_tokens,
        "stream": True,
        "stream_options": {"include_usage": True}
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )

        if response.status_code != 200:
            yield f"LỖI API ({response.status_code}): {response.text}"
            return

        final_usage = None
        for line in response.iter_lines():
            if not line:
                continue
            line_str = line.decode("utf-8")
            if line_str.startswith("data: "):
                data_part = line_str[6:].strip()
                if data_part == "[DONE]":
                    break
                try:
                    data_json = json.loads(data_part)
                    
                    # Kiểm tra usage ở chunk cuối
                    if "usage" in data_json and data_json["usage"]:
                        final_usage = data_json["usage"]

                    choices = data_json.get("choices", [])
                    if choices and len(choices) > 0:
                        delta = choices[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield content
                except Exception:
                    continue

        # Trả về usage ở cuối cùng dưới dạng dictionary đặc biệt
        if final_usage:
            yield {"__usage__": final_usage}
        else:
            # Ước tính nếu API không gửi kèm
            yield {"__usage__": {"prompt_tokens": 500, "completion_tokens": 300}}

    except Exception as e:
        yield f"LỖI KẾT NỐI: {str(e)}"
