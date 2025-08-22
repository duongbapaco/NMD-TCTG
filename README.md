# 📊 Dashboard Công tơ NMĐ (Streamlit + EasyOCR)

Ứng dụng đọc dữ liệu từ ảnh công tơ, so sánh với danh sách trong Excel và tính toán **định mức kinh tế kỹ thuật**.

## 🚀 Hướng dẫn deploy trên Streamlit Cloud

1. Tạo repo mới trên GitHub, upload toàn bộ file:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - (thêm file Excel mẫu nếu cần)

2. Vào [Streamlit Cloud](https://share.streamlit.io/), chọn **New app** → kết nối GitHub repo.

3. Chọn:
   - **Repository**: repo vừa tạo
   - **Branch**: main
   - **File path**: `app.py`

4. Bấm **Deploy** 🚀

## 📸 Cách sử dụng
- Upload file Excel danh sách công tơ (gồm cột *Tên công tơ*, *Lượng nước*, *Lượng khí*).
- Upload ảnh công tơ (jpg/png).
- Hệ thống sẽ OCR dữ liệu, tính toán định mức:
  - **Đỏ** nếu định mức > 1.15 (cảnh báo)
  - **Xanh** nếu định mức ≤ 1.15 (tốt).
- Xuất file kết quả Excel.

## 🛠️ Yêu cầu
- Python 3.9+
- Các gói trong `requirements.txt`
