from .chatbot import FoodChatbot


def main():
    bot = FoodChatbot()
    print("=== Chatbot đặt món ăn ===")
    print("Gõ 'quit' hoặc 'exit' để thoát.\n")

    while True:
        try:
            user = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTạm biệt!")
            break

        if user.lower() in {"quit", "exit"}:
            print("Chatbot: Dạ, em chào anh/chị ạ!")
            break

        if not user:
            continue

        try:
            reply = bot.handle(user)
        except Exception as e:
            reply = f"Xin lỗi, hệ thống đang gặp lỗi: {e}"

        print(f"Chatbot: {reply}\n")


if __name__ == "__main__":
    main()
