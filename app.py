import streamlit as st
import cv2
import pytesseract
from PIL import Image
import numpy as np

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Page configuration
st.set_page_config(
    page_title="Smart OCR",
    page_icon="🔎",
    layout="wide"
)

# Title
st.title("🔎 Smart OCR")
st.subheader("Optical Character Recognition System")

st.write(
    "Upload an image and extract the text automatically using OCR."
)

# Sidebar
st.sidebar.header("⚙️ OCR Settings")

psm = st.sidebar.selectbox(
    "Page segmentation mode",
    [3, 6, 11],
    index=1
)

preprocess = st.sidebar.checkbox(
    "Improve image before OCR",
    value=True
)

# Upload
uploaded_file = st.file_uploader(
    "📤 Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    # Read image
    image = Image.open(uploaded_file)

    # Two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Original Image")
        st.image(image, use_container_width=True)

    # Convert image to OpenCV
    img_array = np.array(image)

    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(
            img_array,
            cv2.COLOR_RGB2GRAY
        )
    else:
        gray = img_array

    # Preprocessing
    if preprocess:

        gray = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        processed = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

    else:
        processed = gray

    with col2:
        st.subheader("✨ Processed Image")
        st.image(
            processed,
            use_container_width=True
        )

    # OCR button
    if st.button(
        "🚀 Extract Text",
        use_container_width=True
    ):

        with st.spinner("Reading text..."):

            config = f"--psm {psm}"

            text = pytesseract.image_to_string(
                processed,
                config=config
            )

        st.success("Text extraction completed!")

        st.subheader("📝 Extracted Text")

        st.text_area(
            "OCR Result",
            text,
            height=300
        )

        # Download
        st.download_button(
            label="⬇️ Download Text",
            data=text,
            file_name="ocr_result.txt",
            mime="text/plain",
            use_container_width=True
        )