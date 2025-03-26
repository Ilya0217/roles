import random
from api.client import send_request_to_api
from spinner import Spinner

def start_dialogue(characters, api_key, model, is_deepseek):
    """Запускает интерактивный диалог между персонажами"""
    print("\nДиалог начался! (нажмите 3 для продолжения, q для выхода)")

    # Первая реплика
    current_speaker = random.choice(list(characters.keys()))
    print(f"\n{characters[current_speaker]['name']}: {characters[current_speaker]['last_response']}")

    while True:
        user_input = input("\n> ")

        if user_input.lower() == 'q':
            print("Диалог завершён.")
            break

        elif user_input == '3':
            spinner = Spinner()
            spinner.start("Генерирую ответ")

            # Выбираем нового говорящего (не того же самого)
            next_speaker = random.choice([k for k in characters.keys() if k != current_speaker])

            # Формируем вопрос
            prompt = f"{characters[current_speaker]['name']} говорит: {characters[current_speaker]['last_response']}\n\n{characters[next_speaker]['name']}, что ответишь?"

            # Получаем ответ
            response = send_request_to_api(
                api_key,
                model,
                prompt,
                characters[next_speaker]['prompt'],
                is_deepseek
            )

            spinner.stop()

            if response:
                # Очищаем ответ от лишнего
                clean_response = response.replace(f"{characters[next_speaker]['name']}:", "").strip()
                print(f"\n{characters[next_speaker]['name']}: {clean_response}")
                characters[next_speaker]['last_response'] = clean_response
                current_speaker = next_speaker
            else:
                print(f"\n{characters[next_speaker]['name']}: *молчит*")

        else:
            print("Неверная команда. Нажмите 3 для продолжения или q для выхода")
