# Optical-Character-Recognition-
This project develops an Optical Character Recognition (OCR) system that extracts text from images and converts it into editable digital text. Using Python, OpenCV, Tesseract OCR, and Streamlit, the system preprocesses images, recognizes text, displays results, and allows users to download the extracted content.
# 🔎 Smart OCR — Optical Character Recognition System

A simple and user-friendly **Optical Character Recognition (OCR)** web application that extracts text from images and converts it into editable digital text.

The project uses **Python, OpenCV, Tesseract OCR, and Streamlit** to provide an interactive OCR experience with image preprocessing and text extraction.

## ✨ Features

* 📤 Upload JPG, JPEG, and PNG images
* 📷 Preview the original image
* 🧹 Image preprocessing for improved recognition
* 🔤 Extract text using Tesseract OCR
* ⚙️ Select OCR page segmentation mode
* 📝 Display extracted text
* ⬇️ Download extracted text as a `.txt` file
* 🌐 Simple and responsive web interface

## 🛠️ Technologies Used

* **Python 3.11+**
* **OpenCV** — Image processing
* **Tesseract OCR** — Text recognition
* **Pytesseract** — Python wrapper for Tesseract
* **NumPy** — Image/data processing
* **Pillow** — Image handling
* **Streamlit** — Web application interface

## 📂 Project Structure

```text
OCR-PROJECT/
│
├── venv/
│
├── images/
│
├── app.py
├── test.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ocr-project.git
cd ocr-project
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install streamlit opencv-python pytesseract pillow numpy
```

## 🔧 Tesseract OCR Setup

This project requires the **Tesseract OCR engine** to be installed separately.

After installing Tesseract on Windows, you may need to specify its location in `app.py`:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

Make sure this path matches the location of `tesseract.exe` on your computer.

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your web browser.

## 🔄 How It Works

```text
        📷 Upload Image
               │
               ▼
       🧹 Image Preprocessing
               │
               ▼
          🔤 Tesseract OCR
               │
               ▼
        📝 Extracted Text
               │
               ▼
         ⬇️ Download Text
```

## 📸 Application Workflow

1. Upload an image containing text.
2. The application displays the original image.
3. Image preprocessing is performed to improve OCR quality.
4. Tesseract analyzes the image.
5. Recognized text is displayed on the screen.
6. The extracted text can be downloaded as a text file.

## 🚀 Future Improvements

The project can be extended with:

* 🌍 Multiple language support
* 📄 PDF document processing
* ✍️ Handwritten text recognition
* 📊 OCR confidence scores
* ✂️ Image cropping
* 🔄 Image rotation and deskewing
* 📋 Copy-to-clipboard functionality
* 📑 Export to PDF or Word
* 🤖 Deep-learning-based OCR
* 📱 Mobile-friendly interface

## 🎯 Applications

This OCR system can be useful for:

* 📚 Digitizing books and notes
* 🏢 Office document processing
* 🧾 Converting receipts into digital text
* 📄 Scanned document processing
* 🎓 Educational projects
* 🗃️ Document archiving
* 🔎 Searching text within images

## 👨‍💻 Author

**Your Name**

Developed as an **Optical Character Recognition project** using Python and computer vision technologies.

## 📄 License

This project is available for educational and personal use.
