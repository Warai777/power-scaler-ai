from chapter_parser.mangadex_image_fetcher import download_mangadex_images
from ocr_on_demand_parser import extract_text_from_images_temp

def fetch_mangadex_chapter(series_name, chapter_number):
    """
    Downloads manga pages from MangaDex and extracts feats using OCR.

    Parameters:
    - series_name (str): The title of the manga
    - chapter_number (int): The chapter number to fetch

    Returns:
    - str: OCR-extracted text of feats, or None if failed
    """
    try:
        # Download chapter images
        image_paths = download_mangadex_images(series_name, chapter_number)
        if not image_paths:
            print(f"[❌] No images found for chapter {chapter_number}")
            return None

        print(f"[🧠] Extracting OCR text from {len(image_paths)} MangaDex pages...")
        
        # Perform OCR on downloaded images
        return extract_text_from_images_temp(image_paths)

    except Exception as e:
        print(f"[MangaDex Fetch Error] {e}")
        return None
