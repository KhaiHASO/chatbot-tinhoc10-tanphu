# 🎤 TÀI LIỆU HƯỚNG DẪN THUYẾT TRÌNH & TRẢ LỜI VẤN ĐÁP
> **Dành riêng cho hai bạn:** Phan Trọng Hiếu & Phạm Mạnh Long  
> **Lớp:** 10A11 — THPT Tân Phú  
> **Đề tài:** Xây dựng Trợ lý Trí tuệ Nhân tạo hỗ trợ học tập môn Tin học lớp 10 (Bộ sách Kết nối tri thức với cuộc sống)

---

## 🎯 PHẦN 1: KỊCH BẢN THUYẾT TRÌNH TRƯỚC LỚP VÀ THẦY CÔ (3 – 5 PHÚT)

### 1. Lời mở đầu (1 phút)
> *"Kính thưa quý Thầy/Cô và các bạn học sinh lớp 10A11,*  
> *Em tên là [Phan Trọng Hiếu / Phạm Mạnh Long], đại diện nhóm nghiên cứu đề tài ứng dụng Tin học của lớp. Trong chương trình Tin học lớp 10, chúng em được tiếp cận với rất nhiều chủ đề mới như hệ nhị phân, dữ liệu logic, đồ họa vector Inkscape và đặc biệt là ngôn ngữ lập trình Python. Trong quá trình học, nhiều bạn thường gặp khó khăn khi nhớ cú pháp, cách chạy vòng lặp hay tìm lỗi khi viết code.*  
> *Xuất phát từ nhu cầu thực tế đó, nhóm em đã nghiên cứu và phát triển sản phẩm: **Trợ lý AI Học tập Tin học 10 (KNTT)** nhằm hỗ trợ thầy cô và các bạn tự học, ôn tập mọi lúc mọi nơi."*

### 2. Điểm đặc biệt của sản phẩm (2 phút)
> *"Sản phẩm của chúng em sở hữu 3 điểm đột phá chính so với các chatbot thông thường:*  
> * **Thứ nhất, tính chuẩn xác sư phạm:** Chatbot được tích hợp kho tri thức từ toàn bộ 34 bài giảng SGK Tin học 10 Kết nối tri thức. Nhờ công nghệ trích xuất ngữ cảnh thông minh, khi học sinh hỏi bất kỳ bài nào, AI sẽ đối chiếu trực tiếp slide bài đó để đưa ra câu trả lời chuẩn kiến thức chương trình.*  
> * **Thứ hai, tính an toàn và bảo mật:** Toàn bộ API Key được bảo vệ an toàn ở máy chủ backend, giao diện có mã PIN lớp học `10A11` để tránh bị bot bên ngoài spam.*  
> * **Thứ ba, cơ chế quản lý chi phí thông minh:** Hệ thống có thanh giám sát ngân sách thời gian thực với tính năng tự động ngắt kết nối an toàn khi chạm ngưỡng định mức, đảm bảo chi phí vận hành cực kỳ tiết kiệm."*

### 3. Demo trực tiếp và Kết luận (1-2 phút)
> *(Chiếu màn hình giao diện web chatbot lên máy chiếu)*  
> * **Thử nghiệm 1:** Bấm vào nút gợi ý *"Vòng lặp for & range()"* -> Cho thầy cô xem AI giải thích cú pháp và code Python có chú thích màu sắc rất rõ ràng.  
> * **Thử nghiệm 2:** Hỏi về *"Cách đổi số 25 sang hệ nhị phân trong Bài 4"* -> Cho thầy cô xem AI chia từng bước chia 2 lấy phần dư theo đúng phương pháp SGK.  
> * **Kết luận:** *"Chúng em xin cảm ơn Thầy/Cô đã lắng nghe và rất mong nhận được những góp ý quý báu để hoàn thiện sản phẩm tốt hơn nữa ạ!"*

---

## 💡 PHẦN 2: BỘ CÂU HỎI THẦY CÔ CÓ THỂ HỎI & GỢI Ý CÂU TRẢ LỜI

### ❓ Câu hỏi 1: *"Chatbot này khác gì việc các em lên ChatGPT hay Google để hỏi?"*
* **Trả lời:**  
  *"Thưa thầy/cô, ChatGPT thông thường là mô hình ngôn ngữ chung, đôi khi sẽ trả lời bằng kiến thức nâng cao, dùng thư viện ngoài không có trong SGK lớp 10, hoặc giải thích sai phương pháp dạy của chương trình Kết nối tri thức. Còn chatbot của chúng em được nạp ngữ cảnh cụ thể từ đúng 34 bài học SGK Tin 10 KNTT, nên câu trả lời luôn bám sát chuẩn thuật ngữ và phạm vi kiến thức mà thầy cô giảng dạy trên lớp ạ."*

### ❓ Câu hỏi 2: *"Các em đã giải quyết bài toán chi phí và hạn ngạch token như thế nào?"*
* **Trả lời:**  
  *"Dạ thưa thầy/cô, chúng em áp dụng giải pháp tối ưu ngữ cảnh (Zero-cost RAG). Thay vì gửi toàn bộ 34 bài học trong mỗi lượt chat (rất tốn token), hệ thống sẽ tìm kiếm và chỉ trích xuất đúng slide bài học liên quan nhất (~500 tokens). Ngoài ra, ở tầng backend chúng em lập trình một module `quota_manager` có chốt ngắt cứng (kill-switch) ghi nhận từng token thực tế, tự động khóa API khi đạt ngưỡng bảo vệ để không bao giờ phát sinh chi phí ngoài ý muốn ạ."*

### ❓ Câu hỏi 3: *"Các em bảo mật hệ thống như thế nào để người ngoài không phá?"*
* **Trả lời:**  
  *"Dạ, chúng em thiết kế 3 tầng bảo mật:*  
  *1. API Key hoàn toàn được giấu trong biến môi trường bảo mật của máy chủ, không bao giờ lộ ra mã nguồn giao diện.*  
  *2. Có mã PIN lớp học `10A11` ở thanh bên trái, chỉ những ai có mã mới gửi được tin nhắn.*  
  *3. Có cơ chế giới hạn tần suất gửi tin nhắn (rate limiting) để chống gửi tin dồn dập tự động ạ."*

### ❓ Câu hỏi 4: *"Nếu học sinh hỏi các câu hỏi không liên quan đến Tin học thì sao?"*
* **Trả lời:**  
  *"Dạ trong System Prompt, chúng em đã cài đặt quy tắc sư phạm nghiêm ngặt: nếu học sinh hỏi chuyện phiếm, chơi game hoặc các chủ đề lạc đề, trợ lý AI sẽ lịch sự từ chối và hướng dẫn bạn quay lại nội dung bài học Tin học 10 ạ."*
