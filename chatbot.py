import openai

openai.api_key = "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"  # 🔑 Thay bằng API key thực

def load_context():
    with open("data/thongbao.txt", "r", encoding="utf-8") as f:
        return f.read()

def ask_chatbot(user_input):
    context = load_context()

    messages = [
        {"role": "system", "content": "Bạn là trợ lý ảo tư vấn tuyển sinh của Trường Đại học Kinh tế - Kỹ thuật Công nghiệp (UNETI). Trả lời dựa trên nội dung sau:\n" + context},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )

    reply = response.choices[0].message.content
    return reply

# Example use
if __name__ == "__main__":
    user_q = input("👤 Bạn hỏi gì về tuyển sinh UNETI? ")
    reply = ask_chatbot(user_q)
    print("🤖 Bot:", reply)
