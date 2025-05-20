import pytesseract
from PIL import Image
import os

def extract_text_from_image(image_path):
    """
    Performs OCR on the given image file and returns extracted text.
    """
    if not os.path.exists(image_path):
        return f"⚠️ Image file not found: {image_path}"

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"❌ OCR failed for {image_path}: {e}"

def extract_text_from_folder(folder_path):
    """
    Scans all .png/.jpg/.jpeg files in a folder and returns combined OCR text.
    """
    if not os.path.isdir(folder_path):
        return f"⚠️ Folder not found: {folder_path}"

    combined_text = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(folder_path, filename)
            text = extract_text_from_image(path)
            if text:
                combined_text.append(f"[Image: {filename}]\n{text}")

    return "\n\n".join(combined_text)
