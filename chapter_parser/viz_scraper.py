import os
from chapter_parser.viz_image_fetcher import download_viz_images 
from ocr_on_demand_parser import extract_text_from_images_temp

# Simulated function that downloads Viz manga chapter images into a temp folder
def download_viz_images(series_name, chapter_number):
    """
    Stub function to simulate Viz image fetching.
    In production, replace this with real scraping or automation (e.g. Playwright headless browser).
    """
    folder = f"ocr/viz/{series_name.lower().replace(' ', '_')}/chapter_{chapter_number}"
    if not os.path.exists(folder):
        print(f"[Viz] ❌ No local Viz images found: {folder}")
        return None

    image_files = [
        os.path.join(folder, f) for f in sorted(os.listdir(folder))
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    if not image_files:
        print(f"[Viz] ❌ No image files found in {folder}")
        return None

    print(f"[Viz] ✅ Found {len(image_files)} page(s) for OCR in: {folder}")
    return image_files


def fetch_viz_chapter(series_name, chapter_number):
    try:
        images = download_viz_images(series_name, chapter_number)
        if not images:
            return None
        return extract_text_from_images_temp(images)
    except Exception as e:
        print(f"[Viz Fetch Error] {e}")
        return None
