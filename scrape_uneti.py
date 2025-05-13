import requests
from bs4 import BeautifulSoup

def scrape_uneti_news():
    url = "https://uneti.edu.vn/category/thong-bao/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = soup.select("h3.post-title > a")
    content_list = []

    for item in news_items[:10]:  # Lấy 5 bài mới nhất
        title = item.text.strip()
        link = item['href']
        article_res = requests.get(link)
        article_soup = BeautifulSoup(article_res.text, 'html.parser')
        paragraphs = article_soup.select("div.td-post-content p")
        article_text = "\n".join(p.get_text().strip() for p in paragraphs[:5])
        content_list.append(f"📰 {title}\n{article_text}\n---")

    full_text = "\n\n".join(content_list)

    with open("data/thongbao.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    print("✅ Đã lưu thông báo mới nhất vào file.")
