import openai
from config import MODELS

def send_request_to_api(api_key, model_name, prompt, role_prompt, is_deepseek=True):
    config = MODELS['deepseek'] if is_deepseek else MODELS['chatgpt']
    
    # Настройка API
    openai.api_key = api_key
    openai.api_base = config['base_url']

    try:
        response = openai.ChatCompletion.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None