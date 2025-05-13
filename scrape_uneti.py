import requests
from bs4 import BeautifulSoup

def scrape_uneti():
    url = "https://uneti.edu.vn/category/thong-bao/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    news = soup.select("h3.post-title a")  # Kiểm tra selector
    print(f"🔍 Tổng số bài viết tìm thấy: {len(news)}")  # THÊM DÒNG NÀY

    contents = []
    for item in news[:5]:
        title = item.get_text(strip=True)
        link = item['href']
        print(f"📄 Đang lấy: {title} - {link}")  # THÊM DÒNG NÀY

        try:
            article = requests.get(link)
            article_soup = BeautifulSoup(article.text, "html.parser")
            body = article_soup.select("div.td-post-content p")
            content = "\n".join(p.get_text(strip=True) for p in body[:3])
            contents.append(f"📰 {title}\n{content}\n---")
        except Exception as e:
            print(f"⚠️ Lỗi khi lấy bài {title}: {e}")

    # Nếu không có gì được scrape
    if not contents:
        print("⚠️ Không lấy được nội dung nào. Có thể cấu trúc HTML đã thay đổi.")
    else:
        with open("data/thongbao.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(contents))
        print("✅ Đã cập nhật dữ liệu tuyển sinh mới nhất.")
