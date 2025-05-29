import openai
from config import MODELS
import sys

def send_request_to_api(api_key, model_name, prompt, role_prompt, is_deepseek=True):
    if not api_key:
        print("Ошибка: API ключ не предоставлен")
        return None
        
    config = MODELS['deepseek'] if is_deepseek else MODELS['chatgpt']
    
    try:
        # Настройка API
        client = openai.OpenAI(
            api_key=api_key,
            base_url=config['base_url']
        )

        response = client.chat.completions.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": role_prompt + "\nОтвечай кратко, максимум 2-3 предложения."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,  # Ограничиваем длину ответа
            temperature=0.7  # Делаем ответы более предсказуемыми
        )
        return response.choices[0].message.content
        
    except openai.AuthenticationError as e:
        print(f"Ошибка аутентификации API: {e}")
        print("Проверьте правильность API ключа")
        return None
    except openai.APIConnectionError as e:
        print(f"Ошибка подключения к API: {e}")
        print("Проверьте подключение к интернету")
        return None
    except openai.RateLimitError as e:
        print(f"Превышен лимит запросов: {e}")
        print("Подождите немного и попробуйте снова")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка API: {e}")
        return None