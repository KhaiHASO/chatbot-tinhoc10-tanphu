#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script trích xuất và chuẩn hóa nội dung 34 bài giảng Tin học 10 (Kết nối tri thức)
từ thư mục PDF để làm Knowledge Base cho Chatbot.
"""

import os
import re
import json
import pymupdf as fitz

PDF_DIR = "/Users/admin/Library/CloudStorage/GoogleDrive-khaikhai331@gmail.com/My Drive/TRAN DAI NGHIA/TIN10-KNTT/TIN10-KNTT/pdf"
OUTPUT_DIR = "/Users/admin/Desktop/DuAnHoTroHS/data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "tin10_knowledge.json")

def get_topic(lesson_num):
    if 1 <= lesson_num <= 7:
        return "Chủ đề 1: Máy tính và xã hội tri thức"
    elif 8 <= lesson_num <= 11:
        return "Chủ đề 2: Mạng máy tính và Internet"
    elif 12 <= lesson_num <= 15:
        return "Chủ đề 3: Đồ họa máy tính (Inkscape)"
    elif 16 <= lesson_num <= 32:
        return "Chủ đề 4: Giải quyết vấn đề với sự trợ giúp của máy tính (Lập trình Python)"
    elif 33 <= lesson_num <= 34:
        return "Chủ đề 5: Hướng nghiệp với Tin học"
    return "Kiến thức chung Tin học 10"

def clean_text(text):
    # Remove multiple spaces, normalize newlines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)

def extract_title(slides_text, lesson_num):
    # Check slide 1 or slide 2 for title
    first_slide = slides_text[0] if slides_text else ""
    lines = [l.strip() for l in first_slide.split("\n") if l.strip()]
    
    # Try to find "BÀI XX:" pattern
    combined = " ".join(lines)
    m = re.search(r"BÀI\s*\d+\s*[:\-–]?\s*([^–\-\n]+)", combined, re.IGNORECASE)
    if m:
        title_part = m.group(1).strip()
        # Clean up if title has extra words
        title_part = re.sub(r"\s+", " ", title_part)
        return f"Bài {lesson_num}: {title_part}"
    
    # Fallback to first few lines
    clean_lines = [l for l in lines if not re.match(r"^\d+$", l) and "TRẦN ĐẠI NGHĨA" not in l.upper()]
    return f"Bài {lesson_num}: {' '.join(clean_lines[:2])}"

def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    def lesson_sort_key(name):
        m = re.search(r"B(\d+)", name)
        return int(m.group(1)) if m else 999
    
    files = sorted(files, key=lesson_sort_key)
    print(f"Tìm thấy {len(files)} file bài học PDF.")
    
    lessons_data = []
    
    for f in files:
        m = re.search(r"B(\d+)", f)
        if not m:
            continue
        lesson_num = int(m.group(1))
        file_path = os.path.join(PDF_DIR, f)
        
        doc = fitz.open(file_path)
        slides_text = []
        for page_idx in range(len(doc)):
            page_text = doc[page_idx].get_text()
            cleaned_page = clean_text(page_text)
            if cleaned_page:
                slides_text.append(cleaned_page)
        
        raw_full_text = "\n\n".join([f"[Slide {i+1}]\n{st}" for i, st in enumerate(slides_text)])
        title = extract_title(slides_text, lesson_num)
        topic = get_topic(lesson_num)
        
        # Tạo tóm tắt cốt lõi
        summary_lines = []
        for st in slides_text[:5]:
            for line in st.split("\n"):
                if any(kw in line.lower() for kw in ["mục tiêu", "khái niệm", "lưu ý", "cú pháp", "ghi nhớ", "kết luận"]):
                    summary_lines.append(line)
        summary = "\n".join(summary_lines[:6]) if summary_lines else "Kiến thức trọng tâm bài học."
        
        lesson_obj = {
            "id": f"B{lesson_num}",
            "lesson_num": lesson_num,
            "filename": f,
            "title": title,
            "topic": topic,
            "total_slides": len(doc),
            "summary": summary,
            "content": raw_full_text
        }
        lessons_data.append(lesson_obj)
        print(f"Đã xử lý Bài {lesson_num}: {title} ({len(doc)} slides)")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(lessons_data, out, ensure_ascii=False, indent=2)
    
    print(f"\n=> Đã lưu thành công dữ liệu 34 bài học vào: {OUTPUT_FILE}")
    print(f"Kích thước file JSON: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")

if __name__ == "__main__":
    run()
