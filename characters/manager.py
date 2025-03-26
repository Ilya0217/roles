from .prompts import ROLE_PROMPTS, NAME_MAPPING
from api.client import send_request_to_api
from spinner import Spinner

def get_character_name(role):
    return NAME_MAPPING.get(role, role)

def initialize_characters(api_key, model, is_deepseek):
    spinner = Spinner()
    spinner.start("Инициализация персонажей")

    characters = {}

    for role_name, prompt in ROLE_PROMPTS.items():
        init_prompt = f"Ты {role_name}. Представься своим одноклассникам."
        response = send_request_to_api(api_key, model, init_prompt, prompt, is_deepseek)

        characters[role_name] = {
            'name': get_character_name(role_name),
            'prompt': prompt,
            'last_response': response or f"Я {get_character_name(role_name)}. Привет!"
        }

    spinner.stop()
    print("\n✓ Все персонажи инициализированы")
    return characters  # Важно: возвращаем созданный словарь
