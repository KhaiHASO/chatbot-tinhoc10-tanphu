# -*- coding: utf-8 -*-
"""
Trợ lý AI Học tập Tin học 10 - Bộ sách Kết nối tri thức với cuộc sống
Đề tài nghiên cứu & ứng dụng:
Học sinh thực hiện: Phan Trọng Hiếu & Phạm Mạnh Long - Lớp 10A11
Đơn vị: Trường THPT Tân Phú
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Nạp các module nghiệp vụ
from knowledge_base import kb
from quota_manager import quota_mgr
from deepseek_client import generate_chat_stream

load_dotenv()

# Cấu hình giao diện trang
st.set_page_config(
    page_title="AI Chatbot Tin Học 10 - KNTT | Lớp 10A11",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho phong cách học đường hiện đại
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        color: #E0E7FF;
        font-size: 0.95rem;
        margin-bottom: 0.2rem;
    }
    .student-badge {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.2);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 0.8rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Lấy cấu hình PIN từ secrets hoặc env
DEFAULT_PIN = os.getenv("ACCESS_PIN", "10A11")
try:
    if "ACCESS_PIN" in st.secrets:
        DEFAULT_PIN = st.secrets["ACCESS_PIN"]
except Exception:
    pass

# Quản lý session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 **Xin chào thầy cô và các bạn!**\n\nMình là **Trợ lý AI Tin học 10 (KNTT)**, sản phẩm được phát triển bởi **Phan Trọng Hiếu** và **Phạm Mạnh Long** (Lớp 10A11 - THPT Tân Phú).\n\nMình đã được nạp toàn bộ kiến thức chuẩn từ **34 bài học SGK Tin học 10 (Kết nối tri thức)**. Bạn có thể hỏi mình về:\n* 🐍 **Lập trình Python:** Cú pháp, vòng lặp, mảng list, hàm, giải thích code và tìm lỗi.\n* 🔢 **Hệ thống dữ liệu:** Hệ nhị phân, dữ liệu logic, bảng chân trị.\n* 🌐 **Mạng & An toàn số:** Bản quyền số, an toàn thông tin mạng.\n* 🎨 **Đồ họa Inkscape:** Khái niệm vector và các thao tác thiết kế.\n\n*Hãy nhập câu hỏi vào ô chat bên dưới hoặc chọn gợi ý bên thanh công cụ nhé!*"
        }
    ]

# --- SIDEBAR: Thông tin & Kiểm soát an toàn ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("⚙️ Bảng Điều Khiển")
    
    # 1. Xác thực mã PIN
    st.subheader("🔐 Xác thực truy cập")
    if not st.session_state.authenticated:
        pin_input = st.text_input("Nhập mã PIN lớp học:", type="password", help="Mã PIN do học sinh/thầy cô thiết lập để chống spam.")
        if st.button("Xác nhận PIN", use_container_width=True):
            if pin_input.strip() == DEFAULT_PIN:
                st.session_state.authenticated = True
                st.success("✅ Đã mở khóa quyền trò chuyện!")
                st.rerun()
            else:
                st.error("❌ Mã PIN không chính xác. Vui lòng liên hệ lớp 10A11!")
    else:
        st.success("✅ Đã xác thực lớp 10A11")
        if st.button("Đăng xuất PIN", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
            
    st.divider()

    # 2. Giám sát ngân sách bảo vệ ($0.20 Hard-Cap)
    st.subheader("🛡️ Giám sát Ngân sách")
    stats = quota_mgr.get_stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Số câu đã hỏi",
            value=f"{stats['total_requests']}/{stats['max_requests']}",
            delta=f"-{stats['remaining_requests']} còn lại"
        )
    with col2:
        st.metric(
            label="Chi phí ước tính",
            value=f"${stats['total_cost_usd']:.4f}",
            delta=f"Cap: ${stats['hard_limit_usd']:.2f}",
            delta_color="inverse"
        )
        
    # Thanh tiến trình chi phí
    st.progress(stats["pct_cost"] / 100.0, text=f"Ngân sách đã dùng: {stats['pct_cost']:.1f}%")
    
    if stats["total_cost_usd"] >= stats["hard_limit_usd"]:
        st.error("🔴 **Đã kích hoạt ngắt an toàn!** Đạt mức bảo vệ $0.18.")
    else:
        st.caption("🟢 Hệ thống đang hoạt động an toàn trong định mức $0.20.")

    st.divider()

    # 3. Tra cứu nhanh 34 bài SGK Tin 10
    st.subheader("📚 Mục lục 34 Bài học")
    all_lessons = kb.get_all_lessons()
    lesson_options = [f"Bài {l['lesson_num']}: {l['title'].split(':', 1)[-1].strip()}" for l in all_lessons]
    selected_idx = st.selectbox("Chọn bài để ôn tập:", range(len(lesson_options)), format_func=lambda x: lesson_options[x])
    
    if st.button("📖 Xem tóm tắt bài này", use_container_width=True):
        sel_lesson = kb.get_lesson_by_num(selected_idx + 1)
        if sel_lesson:
            st.info(f"**{sel_lesson['title']}**\n\n*{sel_lesson['topic']}*\n\n{sel_lesson['summary']}")

    st.divider()
    
    # 4. Tác giả & Đơn vị
    st.caption("🏫 **THPT Tân Phú**")
    st.caption("👥 **Tác giả:** Phan Trọng Hiếu - Phạm Mạnh Long")
    st.caption("🎓 **Lớp:** 10A11 | GV phụ trách Tin học")

# --- MAIN CONTENT ---
# Header dự án
st.markdown("""
<div class="main-header">
    <h1>🤖 TRỢ LÝ AI HỌC TẬP TIN HỌC 10 (KNTT)</h1>
    <p>Hệ thống AI gia sư hỗ trợ học sinh & giải đáp bài tập theo chuẩn SGK Kết nối tri thức với cuộc sống</p>
    <div class="student-badge">
        👨‍🎓 Đề tài thực hiện: <b>Phan Trọng Hiếu & Phạm Mạnh Long</b> — Lớp <b>10A11</b> | THPT Tân Phú
    </div>
</div>
""", unsafe_allow_html=True)

# Gợi ý nhanh các câu hỏi mẫu
st.markdown("##### 💡 Gợi ý câu hỏi nhanh:")
qcols = st.columns(4)
quick_prompt = None

with qcols[0]:
    if st.button("🐍 Vòng lặp for & range()", use_container_width=True):
        quick_prompt = "Em hãy giải thích cú pháp câu lệnh lặp for trong Python (Bài 20) và cho một ví dụ dễ hiểu kèm chú thích từng dòng lệnh."

with qcols[1]:
    if st.button("🔢 Hệ nhị phân là gì?", use_container_width=True):
        quick_prompt = "Hệ nhị phân là gì trong Bài 4 Tin học 10? Hãy hướng dẫn cách đổi một số thập phân như số 25 sang nhị phân."

with qcols[2]:
    if st.button("📋 Kiểu dữ liệu List", use_container_width=True):
        quick_prompt = "Trình bày các lệnh làm việc với danh sách List trong Bài 23 (append, remove, len) và cho ví dụ minh họa."

with qcols[3]:
    if st.button("🐞 Lỗi SyntaxError & Debug", use_container_width=True):
        quick_prompt = "Trong Bài 29 và 30, những lỗi chương trình thường gặp nhất khi mới học Python là gì và cách sửa thế nào?"

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý input từ học sinh (hoặc từ nút gợi ý nhanh)
user_input = st.chat_input("Nhập câu hỏi về môn Tin học 10 tại đây...")
if quick_prompt and not user_input:
    user_input = quick_prompt

if user_input:
    # 1. Kiểm tra xác thực mã PIN
    if not st.session_state.authenticated:
        st.warning("🔒 Vui lòng nhập **Mã PIN lớp học** ở thanh công cụ bên trái (Mặc định: `10A11`) trước khi gửi câu hỏi để tránh spam!")
        st.stop()

    # 2. Kiểm tra hạn ngạch ngân sách
    can_run, reason = quota_mgr.can_proceed()
    if not can_run:
        st.error(reason)
        st.stop()

    # 3. Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 4. Trích xuất ngữ cảnh SGK phù hợp (RAG siêu nhẹ)
    context = kb.search_relevant_context(user_input)

    # 5. Gọi DeepSeek và hiển thị dạng streaming
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        usage_info = None

        # Chuẩn bị lịch sử hội thoại gần nhất (tối đa 4 tin gần nhất để tiết kiệm token)
        history_to_send = []
        for m in st.session_state.messages[-4:]:
            if m["role"] in ["user", "assistant"]:
                history_to_send.append({"role": m["role"], "content": m["content"]})

        stream = generate_chat_stream(history_to_send, context=context, max_tokens=650)
        
        for chunk in stream:
            if isinstance(chunk, dict) and "__usage__" in chunk:
                usage_info = chunk["__usage__"]
            else:
                full_response += str(chunk)
                response_placeholder.markdown(full_response + "▌")
                
        response_placeholder.markdown(full_response)

    # 6. Ghi nhận chi phí và token
    if usage_info:
        p_tokens = usage_info.get("prompt_tokens", 400)
        c_tokens = usage_info.get("completion_tokens", 250)
        call_cost = quota_mgr.record_usage(p_tokens, c_tokens)
    else:
        # Dự phòng nếu không có usage
        call_cost = quota_mgr.record_usage(500, 300)

    # 7. Lưu câu trả lời vào session
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Rerun nhẹ để cập nhật sidebar metric
    st.rerun()
