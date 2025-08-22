import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import os

st.title("📊 Dashboard Đọc & Tính Định Mức")

# --- Upload file Excel ---
uploaded_excel = st.file_uploader("📂 Upload file Excel", type=["xlsx", "xlsm"])
df_meters = None

if uploaded_excel:
    df_meters = pd.read_excel(uploaded_excel)
    st.success("✅ Đã nạp dữ liệu Excel")
    st.dataframe(df_meters)

# --- Upload ảnh ---
uploaded_images = st.file_uploader("📸 Upload ảnh công tơ", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

df_results = pd.DataFrame()

if uploaded_images:
    results = []
    for img_file in uploaded_images:
        img = Image.open(img_file)
        text = pytesseract.image_to_string(img, lang="eng")  # Tạm OCR tiếng Anh, có thể đổi sang 'vie'
        results.append({"Ảnh": img_file.name, "Giá trị đọc": text.strip()})
    df_results = pd.DataFrame(results)
    st.success("✅ Đã OCR ảnh xong")
    st.dataframe(df_results)

# --- Ghép dữ liệu ---
if df_meters is not None:
    st.subheader("🔍 Kiểm tra cột trong dữ liệu")
    st.write("📊 Excel có cột:", df_meters.columns.tolist())
    st.write("📸 OCR có cột:", df_results.columns.tolist())

    if "Tên công tơ" in df_meters.columns and "Ảnh" in df_results.columns:
        df_final = pd.merge(
            df_meters, df_results, left_on="Tên công tơ", right_on="Ảnh", how="left"
        )

        # --- Tính định mức ---
        if "Lượng nước" in df_final.columns and "Lượng khí" in df_final.columns:
            df_final["Định mức (tấn/h)"] = (
                df_final["Lượng nước"].diff() / df_final["Lượng khí"]
            )

            # --- Cảnh báo màu ---
            def color_rate(val):
                try:
                    if val > 1.15:
                        return "background-color: red; color: white;"
                    else:
                        return "background-color: green; color: white;"
                except:
                    return ""

            st.subheader("📊 Kết quả cuối cùng")
            st.dataframe(df_final.style.applymap(color_rate, subset=["Định mức (tấn/h)"]))
        else:
            st.error("⚠️ Excel chưa có đủ cột 'Lượng nước' và 'Lượng khí' để tính định mức")
            df_final = df_meters.copy()

    else:
        st.error("⚠️ Không tìm thấy cột phù hợp để merge. Kiểm tra lại Excel và kết quả OCR.")
        df_final = df_meters.copy()
