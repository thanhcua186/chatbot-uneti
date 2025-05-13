from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import fitz  # PyMuPDF

# Khởi tạo Flask app
app = Flask(__name__)

# Khởi tạo client GPT với API key từ biến môi trường
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Hàm đọc nội dung từ PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"❌ Lỗi đọc PDF {pdf_path}: {e}")
        return ""

# Đọc dữ liệu context từ text + pdf
def load_context():
    context = ""

    # Đọc file text nếu có
    try:
        with open("data/thongbao.txt", "r", encoding="utf-8") as f:
            context += f.read()
    except FileNotFoundError:
        print("⚠️ Không tìm thấy thongbao.txt")

    # Đọc các file PDF (có thể thêm nhiều file vào danh sách này)
    pdf_files = ["data/de-an-tuyen-sinh.pdf", "data/chi-tieu.pdf"]
    for pdf in pdf_files:
        context += "\n\n" + extract_text_from_pdf(pdf)

    return context

# Hàm hỏi GPT
def ask_gpt(question):
    context = load_context()

    messages = [
        {"role": "system", "content": "Bạn là trợ lý ảo tư vấn tuyển sinh của Trường Đại học Kinh tế - Kỹ thuật Công nghiệp (UNETI). Trả lời ngắn gọn, chính xác và dễ hiểu dựa trên nội dung sau:\n" + context},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content

# Trang giao diện chính
@app.route("/")
def index():
    return render_template("index.html")

# API trả lời câu hỏi
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = ask_gpt(question)
    return jsonify({"answer": answer})

# Khởi chạy Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
