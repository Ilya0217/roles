from characters.manager import initialize_characters
from dialogue import start_dialogue
from config import DEEPSEEK_API_KEY, CHATGPT_API_KEY, MODELS

def main():
    print("Выберите нейросеть: 1 - DeepSeek, 2 - ChatGPT")
    choice = input("Ваш выбор: ")

    if choice == '1':
        api_key = DEEPSEEK_API_KEY
        is_deepseek = True
    elif choice == '2':
        api_key = CHATGPT_API_KEY
        is_deepseek = False
    else:
        print("Неверный выбор")
        return

    model = MODELS['deepseek' if is_deepseek else 'chatgpt']['model']
    characters = initialize_characters(api_key, model, is_deepseek)

    if characters:  # Проверяем, что персонажи созданы
        start_dialogue(characters, api_key, model, is_deepseek)
    else:
        print("Ошибка: Не удалось инициализировать персонажей!")

if __name__ == "__main__":
    main()
