from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import requests
from urllib.parse import quote_plus
import re

def fetch_youtube_summary(series_name, chapter_number):
    try:
        query = f"{series_name} chapter {chapter_number} summary"
        search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        response = requests.get(search_url)

        # Use regex to extract video IDs
        video_ids = re.findall(r"watch\\?v=(.{11})", response.text)
        seen = set()
        unique_ids = [x for x in video_ids if not (x in seen or seen.add(x))]

        for vid in unique_ids[:5]:  # Try first few results
            try:
                transcript = YouTubeTranscriptApi.get_transcript(vid, languages=['en'])
                formatter = TextFormatter()
                text = formatter.format_transcript(transcript)
                return text
            except Exception:
                continue

        print("[YouTube] No valid transcript found.")
        return None

    except Exception as e:
        print(f"[YouTube Error] {e}")
        return None
