import os
import requests
from bs4 import BeautifulSoup

def scrape_uneti():
    url = "https://uneti.edu.vn/category/thong-bao/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    news = soup.select("h3.post-title a")
    print(f"🔍 Tổng số bài viết tìm thấy: {len(news)}")

    contents = []
    for item in news[:5]:
        title = item.get_text(strip=True)
        link = item['href']
        print(f"📄 Đang lấy: {title} - {link}")

        try:
            article = requests.get(link)
            article_soup = BeautifulSoup(article.text, "html.parser")
            body = article_soup.select("div.td-post-content p")
            content = "\n".join(p.get_text(strip=True) for p in body[:3])
            contents.append(f"📰 {title}\n{content}\n---")
        except Exception as e:
            print(f"⚠️ Lỗi khi lấy bài {title}: {e}")

    # Tạo thư mục nếu chưa có
    output_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(output_dir, exist_ok=True)

    # Ghi file ra đúng vị trí
    output_path = os.path.join(output_dir, "thongbao.txt")
    if not contents:
        print("⚠️ Không lấy được nội dung nào.")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(contents))
        print("✅ Đã ghi dữ liệu vào:", output_path)
