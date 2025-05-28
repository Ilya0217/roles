# from characters.manager import initialize_characters
# from dialogue import start_dialogue
# from config import DEEPSEEK_API_KEY, CHATGPT_API_KEY, MODELS

# def main():
#     print("Выберите нейросеть: 1 - DeepSeek, 2 - ChatGPT")
#     choice = input("Ваш выбор: ")

#     if choice == '1':
#         api_key = DEEPSEEK_API_KEY
#         is_deepseek = True
#     elif choice == '2':
#         api_key = CHATGPT_API_KEY
#         is_deepseek = False
#     else:
#         print("Неверный выбор")
#         return

#     model = MODELS['deepseek' if is_deepseek else 'chatgpt']['model']
#     characters = initialize_characters(api_key, model, is_deepseek)

#     if characters:  # Проверяем, что персонажи созданы
#         start_dialogue(characters, api_key, model, is_deepseek)
#     else:
#         print("Ошибка: Не удалось инициализировать персонажей!")

# if __name__ == "__main__":
#     main()

from typing import Optional
from characters.manager import initialize_characters
from dialogue import start_dialogue
from config import DEEPSEEK_API_KEY, CHATGPT_API_KEY, MODELS
from analysis.hypothesis import (
    test_leadership_hypothesis,
    test_conflict_hypothesis,
    test_group_formation
)

def main():
    print("Выберите нейросеть:\n1 - DeepSeek\n2 - ChatGPT")
    choice = input("Ваш выбор: ").strip()

    if choice == '1':
        api_key = DEEPSEEK_API_KEY
        model = MODELS['deepseek']['model']
        is_deepseek = True
    elif choice == '2':
        api_key = CHATGPT_API_KEY
        model = MODELS['chatgpt']['model']
        is_deepseek = False
    else:
        print("Неверный выбор. Используйте 1 или 2.")
        return

    characters = initialize_characters(api_key, model, is_deepseek)
    
    if characters:
        print("\nПерсонажи готовы к диалогу!")
        print("Инструкция:\n- Нажмите 3 для следующей реплики\n- Нажмите 1 для выбора тона ответа\n- Нажмите q для выхода\n")

        dialogues = start_dialogue(characters, api_key, model, is_deepseek)
        
        # Анализ результатов
        print("\n" + "="*50)
        print("Итоговый анализ социальной динамики:")
        print("-"*50)
        print(test_leadership_hypothesis(dialogues))
        print(test_conflict_hypothesis(dialogues))
        print(test_group_formation(dialogues))
        print("="*50 + "\n")
    else:
        print("Ошибка: Не удалось инициализировать персонажей!")

if __name__ == "__main__":
    main()
