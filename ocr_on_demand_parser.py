import os
import pytesseract
from PIL import Image

def extract_text_from_folder(folder_path):
    """
    Extracts text from all image files in the given folder using OCR.
    Supported formats: .jpg, .jpeg, .png

    Returns:
        str: Combined OCR text from all images.
    """
    if not os.path.exists(folder_path):
        return ""

    combined_text = []
    supported_exts = (".jpg", ".jpeg", ".png")

    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith(supported_exts):
            try:
                img_path = os.path.join(folder_path, file)
                img = Image.open(img_path)
                text = pytesseract.image_to_string(img)
                if text.strip():
                    combined_text.append(f"[{file}]\n{text.strip()}")
            except Exception as e:
                print(f"[OCR Error] Failed to parse {file}: {e}")

    return "\n\n".join(combined_text).strip()

def cleanup_folder(folder_path):
    """Deletes all files in a given folder and removes the folder."""
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            os.remove(os.path.join(folder_path, file))
        os.rmdir(folder_path)


def extract_text_from_images_temp(pages):
    """
    OCRs a list of image file paths and then deletes them after processing.
    This is the core of on-demand OCR.
    
    Args:
        pages (List[str]): List of paths to downloaded image files

    Returns:
        str: Extracted OCR text
    """
    text_output = []
    for path in pages:
        try:
            img = Image.open(path)
            text = pytesseract.image_to_string(img)
            if text.strip():
                text_output.append(f"[{os.path.basename(path)}]\n{text.strip()}")
        except Exception as e:
            print(f"[OCR Error] {path}: {e}")

    # Clean up files
    for path in pages:
        try:
            os.remove(path)
        except:
            pass

    return "\n\n".join(text_output).strip()
