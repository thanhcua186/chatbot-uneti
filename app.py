from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = "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"  # 🔑 Thay bằng key của bạn

def load_context():
    with open("data/thongbao.txt", "r", encoding="utf-8") as f:
        return f.read()

def ask_gpt(question):
    context = load_context()
    messages = [
        {"role": "system", "content": "Bạn là trợ lý tuyển sinh UNETI. Trả lời dựa trên thông tin sau:\n" + context},
        {"role": "user", "content": question}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    answer = ask_gpt(data["question"])
    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
