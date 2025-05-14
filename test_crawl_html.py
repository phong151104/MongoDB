from app.utils.crawler import get_html_from_url

if __name__ == "__main__":
    link = input("Nhập link cần crawl: ").strip()
    html = get_html_from_url(link)
    html_length = len(html) if html else 0
    print("--- HTML Content (first 500 chars) ---")
    print(html[:500] if html else "Không lấy được nội dung.")
    print("\n--- HTML Length ---")
    print(html_length) 