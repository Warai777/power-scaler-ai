from chapter_parser.chapter_parser import parse_chapter
from chapter_parser.anime_parser import parse_anime_episode

def main():
    print("=== Power Scaling Feat Tester ===")
    mode = input("Type 'manga' or 'anime': ").strip().lower()

    if mode not in ["manga", "anime"]:
        print("Invalid mode.")
        return

    series = input("Series title: ").strip()
    number = input("Chapter/Episode number: ").strip()

    try:
        number = int(number)
    except ValueError:
        print("Invalid number.")
        return

    if mode == "manga":
        result = parse_chapter(series, number)
    else:
        result = parse_anime_episode(series, number)

    print("\n=== Parsed Feat Result ===\n")
    print(result)

if __name__ == "__main__":
    main()
