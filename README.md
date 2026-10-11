# 🤖 TRỢ LÝ AI HỌC TẬP TIN HỌC 10 (KNTT)
> **Dự án nghiên cứu & ứng dụng của học sinh lớp 10A11 — Trường THPT Tân Phú**  
> **Tác giả:** Phan Trọng Hiếu & Phạm Mạnh Long  
> **Chương trình:** Tin học lớp 10 — Bộ sách Kết nối tri thức với cuộc sống (34 bài học)

---

## 📌 1. Giới thiệu Đề tài
Dự án được xây dựng nhằm tạo ra một **Gia sư Trí tuệ nhân tạo (AI Chatbot)** chuyên sâu, bám sát 100% chương trình chuẩn SGK Tin học 10 Kết nối tri thức. Trợ lý AI có khả năng:
* Giải thích chi tiết các khái niệm lý thuyết (hệ nhị phân, dữ liệu logic, mạng máy tính, đồ họa vector Inkscape).
* Hướng dẫn giải bài tập lập trình Python căn bản (cú pháp, rẽ nhánh `if`, vòng lặp `for`/`while`, danh sách `list`, xử lý chuỗi, hàm `def`).
* Phân tích và hướng dẫn học sinh sửa các lỗi lập trình phổ biến (`SyntaxError`, `IndentationError`, `IndexError`...).

---

## 🛡️ 2. Cơ chế Bảo mật & Kiểm soát Ngân sách ($0.20 Hard-Cap)
Hệ thống được trang bị **4 lớp bảo vệ an toàn kỹ thuật**:
1. **Lớp 1 - Kill-Switch Ngân sách ($0.18 USD):** Hệ thống ghi nhận chính xác từng token input/output thực tế qua DeepSeek API. Khi tổng chi phí đạt ngưỡng **$0.18 USD**, server sẽ tự động ngắt kết nối API để bảo vệ tài khoản, cam kết không bao giờ vượt quá ngân sách $0.20.
2. **Lớp 2 - Định mức Lượt hỏi (200 câu):** Giới hạn tối đa 200 lượt hỏi phục vụ cho đợt báo cáo và thử nghiệm lớp 10A11.
3. **Lớp 3 - Cơ chế Zero-Cost RAG:** Trích xuất và lập chỉ mục 34 bài SGK thành dữ liệu nhẹ. Mỗi câu hỏi chỉ trích xuất đúng slide của bài học liên quan (~500 tokens), giúp chi phí mỗi câu hỏi giảm xuống mức siêu rẻ (~0.0003 USD / câu).
4. **Lớp 4 - Mã PIN Lớp học (`10A11`):** Chống bot tự động và ngăn người ngoài truy cập làm hao hụt hạn ngạch.

---

## 🚀 3. Hướng dẫn Chạy Thử trên Máy Local (macOS/Windows)

### Bước 1: Mở Terminal tại thư mục dự án
```bash
cd /Users/admin/Desktop/DuAnHoTroHS
```

### Bước 2: Cài đặt thư viện cần thiết (nếu chưa có)
```bash
pip install -r requirements.txt
```

### Bước 3: Khởi chạy ứng dụng
```bash
streamlit run app.py
```
Ứng dụng sẽ tự động mở tại trình duyệt: `http://localhost:8501`.

---

## 🌐 4. Hướng dẫn Triển khai (Deploy) Lên Streamlit Cloud Miễn Phí 100%

Dịch vụ **Streamlit Community Cloud** cho phép đưa ứng dụng lên mạng có link chia sẻ vĩnh viễn (dạng `https://tinhoc10-10a11.streamlit.app`), hoàn toàn miễn phí và không cần nhập thẻ ngân hàng.

### Bước 1: Khởi tạo Git và đẩy code lên GitHub
1. Mở Terminal tại thư mục dự án:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - AI Chatbot Tin hoc 10 KNTT"
   ```
2. Tạo 1 repository mới trên GitHub (ví dụ: `chatbot-tinhoc10-10a11`).
3. Đẩy code lên:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<tai-khoan-github-cua-ban>/chatbot-tinhoc10-10a11.git
   git push -u origin main
   ```
   *(Lưu ý: File `.gitignore` đã tự động ẩn file `.env` và `usage.db` để đảm bảo API key không bao giờ bị lộ ra công cộng).*

### Bước 2: Deploy trên Streamlit Community Cloud
1. Truy cập: [share.streamlit.io](https://share.streamlit.io) và đăng nhập bằng tài khoản GitHub.
2. Bấm nút **"Create app"** (hoặc **"New app"**).
3. Chọn Repository vừa tạo:
   * **Repository:** `chatbot-tinhoc10-10a11`
   * **Branch:** `main`
   * **Main file path:** `app.py`
   * **App URL:** Đặt tên tuỳ chọn (ví dụ: `tinhoc10-10a11`).
4. Nhấn vào mục **"Advanced settings"** -> **"Secrets"**, dán nội dung sau vào:
   ```toml
   DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
   ACCESS_PIN = "10A11"
   HARD_LIMIT_USD = 0.18
   MAX_REQUESTS = 200
   ```
5. Bấm **"Deploy"**!
Chờ khoảng 1-2 phút, ứng dụng sẽ online và có link HTTPS chính thức để gửi thầy cô chấm bài!

---

## 👥 5. Tác giả & Đơn vị thực hiện
* **Học sinh:** Phan Trọng Hiếu & Phạm Mạnh Long
* **Chi đoàn:** 10A11
* **Trường:** THPT Tân Phú
