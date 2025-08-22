import streamlit as st
import pandas as pd
import easyocr
import numpy as np
from PIL import Image

# OCR Reader (khởi tạo chỉ 1 lần)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

st.set_page_config(page_title="Dashboard Công tơ NMĐ", layout="wide")

st.title("📊 Dashboard Công tơ NMĐ - OCR & Định mức")

# --- Upload file Excel danh sách công tơ ---
uploaded_excel = st.file_uploader("📂 Tải lên file Excel danh sách công tơ", type=["xlsx"])
if uploaded_excel:
    df_meters = pd.read_excel(uploaded_excel)
    st.success("✅ Đã tải danh sách công tơ")
    st.dataframe(df_meters)

# --- Upload ảnh công tơ ---
uploaded_images = st.file_uploader("📸 Tải ảnh công tơ", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

results = []

if uploaded_images and uploaded_excel:
    for img_file in uploaded_images:
        image = Image.open(img_file)
        st.image(image, caption=f"Ảnh: {img_file.name}", width=300)

        # OCR
        ocr_texts = reader.readtext(np.array(image), detail=0)
        extracted_text = " ".join(ocr_texts)

        results.append({"Ảnh": img_file.name, "Kết quả OCR": extracted_text})

    df_results = pd.DataFrame(results)

    # Gộp với danh sách công tơ
    df_final = pd.merge(df_meters, df_results, left_on="Tên công tơ", right_on="Ảnh", how="left")

    # --- Tính toán định mức ---
    if "Lượng nước" in df_final.columns and "Lượng khí" in df_final.columns:
        df_final["Định mức (tấn/h)"] = (df_final["Lượng nước"].diff()) / df_final["Lượng khí"]

        # Cảnh báo màu
        def check_status(val):
            if pd.isna(val):
                return ""
            return f"color: {'red' if val > 1.15 else 'green'}; font-weight:bold;"

        st.subheader("📑 Kết quả phân tích")
        st.dataframe(df_final.style.applymap(check_status, subset=["Định mức (tấn/h)"]))

    # Xuất file
    st.download_button(
        "📥 Tải kết quả Excel",
        df_final.to_excel(index=False, engine="openpyxl"),
        file_name="ket_qua_ocr_dinh_muc.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
