from .prompts import ROLE_PROMPTS, NAME_MAPPING, ENVIRONMENT_PROMPTS
from api.client import send_request_to_api
from spinner import Spinner

def get_character_name(role):
    return NAME_MAPPING.get(role, role)

def initialize_characters(api_key, model, is_deepseek, environment):
    spinner = Spinner()
    spinner.start("Инициализация персонажей")

    characters = {}
    env_config = ENVIRONMENT_PROMPTS[environment]

    for role_name, prompt in ROLE_PROMPTS.items():
        # Добавляем контекст окружения к промпту
        env_context = f"\nСейчас {env_config['context']} Настроение: {env_config['mood']}."
        init_prompt = f"Представься кратко (1-2 предложения). Ты {role_name}.{env_context}"
        
        response = send_request_to_api(api_key, model, init_prompt, prompt, is_deepseek)

        characters[role_name] = {
            'name': get_character_name(role_name),
            'prompt': prompt + env_context,  # Добавляем контекст окружения к основному промпту
            'last_response': response or f"Я {get_character_name(role_name)}. Привет!"
        }

    spinner.stop()
    print("\n✓ Все персонажи инициализированы")
    return characters  # Важно: возвращаем созданный словарь

