import os
import asyncio
from playwright.async_api import async_playwright

async def download_viz_images_async(series_name, chapter_number, output_folder):
    safe_name = series_name.lower().replace(" ", "-").replace(":", "").replace(".", "")
    output_path = f"{output_folder}/{safe_name}/chapter_{chapter_number}"
    os.makedirs(output_path, exist_ok=True)

    # Skip if already downloaded
    if os.listdir(output_path):
        print(f"[🔁] Viz pages already exist → {output_path}")
        return output_path

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await context.new_page()

        try:
            # Sample Viz search URL (adjust depending on your target page)
            url = f"https://www.viz.com/shonenjump/chapters/{safe_name}"
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(2000)

            # Click chapter number or navigate directly
            # You may need to fine-tune this depending on how Viz structures chapter URLs
            chapter_links = await page.locator("a").all()
            target_link = None

            for link in chapter_links:
                href = await link.get_attribute("href")
                if href and f"/chapter/{chapter_number}" in href:
                    target_link = href
                    break

            if not target_link:
                print(f"[❌] Chapter {chapter_number} not found on Viz.")
                return None

            full_chapter_url = f"https://www.viz.com{target_link}"
            await page.goto(full_chapter_url)
            await page.wait_for_timeout(3000)

            # Scroll and screenshot all pages
            page_count = 0
            while True:
                img_selector = "img.page-image"
                image = await page.query_selector(img_selector)
                if image:
                    screenshot_path = os.path.join(output_path, f"{page_count + 1:03}.png")
                    await image.screenshot(path=screenshot_path)
                    print(f"[📸] Saved page {page_count + 1}")
                    page_count += 1

                next_btn = await page.query_selector("button.next-page")
                if not next_btn:
                    break
                await next_btn.click()
                await page.wait_for_timeout(1500)

            await browser.close()
            return output_path

        except Exception as e:
            print(f"[❌] Viz Image Fetch Failed: {e}")
            await browser.close()
            return None


def download_viz_images(series_name, chapter_number):
    folder = "ocr/viz"
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(download_viz_images_async(series_name, chapter_number, folder))
