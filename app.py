
import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
import io

# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Smart OCR",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 45px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.result-box {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================

def upscale_image(image, scale=3):
    """
    Upscale image to give OCR more pixels to work with.
    """
    return cv2.resize(
        image,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )


def preprocess_image(image, method):
    """
    Apply different preprocessing techniques.
    """

    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image.copy()

    # Upscale
    gray = upscale_image(gray, 3)

    # Noise reduction
    denoised = cv2.bilateralFilter(
        gray,
        9,
        75,
        75
    )

    # Contrast enhancement
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(denoised)

    # Sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    sharpened = cv2.filter2D(
        enhanced,
        -1,
        kernel
    )

    # Different preprocessing methods
    if method == "Original":
        result = gray

    elif method == "Grayscale":
        result = gray

    elif method == "Enhanced":
        result = enhanced

    elif method == "Sharpened":
        result = sharpened

    elif method == "Otsu":
        result = cv2.threshold(
            sharpened,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

    elif method == "Adaptive":
        result = cv2.adaptiveThreshold(
            sharpened,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            11
        )

    elif method == "Denoised":
        result = denoised

    else:
        result = enhanced

    return result


def perform_ocr(image, psm=6):
    """
    Perform OCR and calculate average confidence.
    """

    config = f"--psm {psm}"

    data = pytesseract.image_to_data(
        image,
        config=config,
        output_type=pytesseract.Output.DICT
    )

    text = pytesseract.image_to_string(
        image,
        config=config
    )

    confidences = []

    for conf in data["conf"]:
        try:
            value = float(conf)

            if value > 0:
                confidences.append(value)

        except (ValueError, TypeError):
            pass

    if confidences:
        average_confidence = sum(confidences) / len(confidences)
    else:
        average_confidence = 0

    return text.strip(), average_confidence


def automatic_ocr(image, psm=6):
    """
    Run OCR using multiple preprocessing methods
    and return the result with the highest confidence.
    """

    methods = [
        "Grayscale",
        "Enhanced",
        "Sharpened",
        "Otsu",
        "Adaptive",
        "Denoised"
    ]

    results = []

    for method in methods:

        processed = preprocess_image(
            image,
            method
        )

        text, confidence = perform_ocr(
            processed,
            psm
        )

        results.append({
            "method": method,
            "image": processed,
            "text": text,
            "confidence": confidence
        })

    # Select highest confidence
    best_result = max(
        results,
        key=lambda x: x["confidence"]
    )

    return best_result, results


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔎 Smart OCR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Advanced Optical Character Recognition for blurry and degraded images'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ OCR Settings")

psm = st.sidebar.selectbox(
    "OCR Page Segmentation",
    [3, 6, 11, 12],
    index=1,
    help="6 works well for a normal block of text."
)

mode = st.sidebar.radio(
    "Processing Mode",
    [
        "Automatic Best Result",
        "Manual Processing"
    ]
)

if mode == "Manual Processing":

    processing_method = st.sidebar.selectbox(
        "Preprocessing Method",
        [
            "Grayscale",
            "Enhanced",
            "Sharpened",
            "Otsu",
            "Adaptive",
            "Denoised"
        ]
    )

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 For blurry images, Automatic Best Result "
    "tests several preprocessing techniques and "
    "selects the result with the highest OCR confidence."
)

# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📤 Upload an image containing text",
    type=["png", "jpg", "jpeg", "bmp", "tiff"]
)

# ============================================================
# MAIN APPLICATION
# ============================================================

if uploaded_file:

    # Open image
    original_pil = Image.open(uploaded_file)

    # Convert to RGB
    original_pil = original_pil.convert("RGB")

    image = np.array(original_pil)

    # Display original
    st.subheader("📷 Original Image")

    st.image(
        original_pil,
        use_container_width=True
    )

    st.markdown("---")

    # ========================================================
    # PROCESS IMAGE
    # ========================================================

    if mode == "Automatic Best Result":

        with st.spinner(
            "🔄 Testing multiple preprocessing techniques..."
        ):

            best_result, all_results = automatic_ocr(
                image,
                psm
            )

        processed = best_result["image"]
        extracted_text = best_result["text"]
        confidence = best_result["confidence"]
        selected_method = best_result["method"]

    else:

        with st.spinner("🔄 Processing image..."):

            processed = preprocess_image(
                image,
                processing_method
            )

            extracted_text, confidence = perform_ocr(
                processed,
                psm
            )

        selected_method = processing_method
        all_results = []

    # ========================================================
    # IMAGE COMPARISON
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📷 Original")

        st.image(
            original_pil,
            use_container_width=True
        )

    with col2:

        st.subheader(
            f"✨ Processed — {selected_method}"
        )

        st.image(
            processed,
            use_container_width=True,
            clamp=True
        )

    # ========================================================
    # CONFIDENCE
    # ========================================================

    st.markdown("---")

    st.subheader("📊 OCR Performance")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "OCR Confidence",
            f"{confidence:.1f}%"
        )

    with col2:

        st.metric(
            "Processing",
            selected_method
        )

    with col3:

        word_count = len(
            extracted_text.split()
        )

        st.metric(
            "Words Detected",
            word_count
        )

    # Confidence progress bar

    confidence_value = max(
        0,
        min(confidence / 100, 1)
    )

    st.progress(
        confidence_value,
        text=f"Confidence: {confidence:.1f}%"
    )

    # ========================================================
    # EXTRACTED TEXT
    # ========================================================

    st.markdown("---")

    st.subheader("📝 Extracted Text")

    if extracted_text:

        edited_text = st.text_area(
            "You can edit the extracted text:",
            value=extracted_text,
            height=300
        )

        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.download_button(
            label="⬇️ Download Text File",
            data=edited_text,
            file_name="ocr_result.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:

        st.warning(
            "⚠️ No text was detected. "
            "Try another image or preprocessing method."
        )

    # ========================================================
    # AUTOMATIC RESULTS
    # ========================================================

    if mode == "Automatic Best Result":

        st.markdown("---")

        st.subheader(
            "🧪 Preprocessing Comparison"
        )

        st.write(
            "The system tested multiple preprocessing "
            "methods and compared their OCR confidence."
        )

        for result in all_results:

            method = result["method"]
            result_confidence = result["confidence"]

            if method == selected_method:

                st.success(
                    f"🏆 {method}: "
                    f"{result_confidence:.1f}% — Selected"
                )

            else:

                st.write(
                    f"• {method}: "
                    f"{result_confidence:.1f}%"
                )

    # ========================================================
    # INFORMATION
    # ========================================================

    st.markdown("---")

    with st.expander("ℹ️ How this OCR system works"):

        st.markdown("""
        ### Processing Pipeline

        **1. Image Upload**
        
        The user uploads an image containing text.

        **2. Upscaling**
        
        The image is enlarged using bicubic interpolation
        to provide more pixels for OCR processing.

        **3. Grayscale Conversion**
        
        Color information is removed so the system can
        focus on text intensity.

        **4. Noise Reduction**
        
        Bilateral filtering reduces noise while attempting
        to preserve character edges.

        **5. Contrast Enhancement**
        
        CLAHE improves text visibility in images with
        uneven lighting.

        **6. Sharpening**
        
        Character edges are enhanced to improve recognition.

        **7. Thresholding**
        
        Otsu and adaptive thresholding convert the image
        into a high-contrast black-and-white representation.

        **8. OCR**
        
        Tesseract analyzes the processed image and extracts
        the detected text.

        **9. Confidence Analysis**
        
        Multiple preprocessing methods can be tested.
        The system selects the result with the highest
        OCR confidence.

        **10. Export**
        
        The extracted text can be edited and downloaded
        as a `.txt` file.
        """)

else:

    # ========================================================
    # WELCOME SCREEN
    # ========================================================

    st.info(
        "👆 Upload an image above to start OCR."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        ### 🧹 Image Enhancement

        Upscaling, denoising, contrast enhancement,
        sharpening and thresholding help improve
        difficult images.
        """)

    with col2:

        st.markdown("""
        ### 🔤 Smart OCR

        Tesseract OCR recognizes text from the
        processed image.
        """)

    with col3:

        st.markdown("""
        ### 📊 Confidence

        Multiple preprocessing methods can be
        compared to find the strongest OCR result.
        """)

