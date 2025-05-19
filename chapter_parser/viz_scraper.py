from playwright.sync_api import sync_playwright
import time

def fetch_viz_chapter(series_name, chapter_number):
    try:
        url = f"https://www.viz.com/shonenjump/chapters/{series_name.replace(' ', '-').lower()}"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)
            page.wait_for_timeout(3000)

            # Find chapter link (match chapter number text in links)
            links = page.locator("a")
            count = links.count()
            chapter_link = None
            for i in range(count):
                href = links.nth(i).get_attribute("href")
                text = links.nth(i).inner_text().lower()
                if f"chapter {chapter_number}" in text:
                    chapter_link = href
                    break

            if not chapter_link:
                print("[Viz] Chapter link not found.")
                return None

            # Go to chapter reader page
            full_url = f"https://www.viz.com{chapter_link}"
            page.goto(full_url)
            page.wait_for_timeout(5000)

            # Try to extract text from visible text boxes
            text_blocks = page.locator(".text-layer div")
            text = []
            for i in range(text_blocks.count()):
                content = text_blocks.nth(i).inner_text().strip()
                if content:
                    text.append(content)

            browser.close()
            return "\n".join(text) if text else None

    except Exception as e:
        print(f"[Viz Error] {e}")
        return None
