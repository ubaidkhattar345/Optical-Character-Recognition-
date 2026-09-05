import cv2
import pytesseract

# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
image = cv2.imread("testpng.jpg")

# Check image
if image is None:
    print("ERROR: Image not found!")
    exit()

# OCR
text = pytesseract.image_to_string(image)

print("Extracted text:")
print(text)