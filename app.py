
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

# Khởi tạo Flask app
app = Flask(__name__)

# Khởi tạo client GPT với API key từ biến môi trường
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Đọc dữ liệu context (ví dụ: thông tin tuyển sinh UNETI)
def load_context():
    with open("data/thongbao.txt", "r", encoding="utf-8") as f:
        return f.read()

# Hàm hỏi GPT
def ask_gpt(question):
    context = load_context()

    messages = [
        {"role": "system", "content": "Bạn là trợ lý tuyển sinh của Trường Đại học Kinh tế - Kỹ thuật Công nghiệp (UNETI). Trả lời ngắn gọn, chính xác và dễ hiểu dựa trên nội dung sau:\n" + context},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content

# Trang chính (chat UI)
@app.route("/")
def index():
    return render_template("index.html")

# Xử lý yêu cầu người dùng
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = ask_gpt(question)
    return jsonify({"answer": answer})

# Chạy app trên Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
