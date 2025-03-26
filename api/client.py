from openai import OpenAI
from config import MODELS

def send_request_to_api(api_key, model_name, prompt, role_prompt, is_deepseek=True):
    config = MODELS['deepseek'] if is_deepseek else MODELS['chatgpt']

    client = OpenAI(
        api_key=api_key,
        base_url=config['base_url']
    )

    try:
        response = client.chat.completions.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}")
        return None
