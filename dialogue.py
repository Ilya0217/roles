# import random
# from api.client import send_request_to_api
# from spinner import Spinner
# from analysis.sentiment import SentimentAnalyzer
# from analysis.graph import InteractionGraph
# from characters.prompts import OBSERVER_PROMPT, TONE_PROMPTS
# from spinner import spinner_context
# from analysis.hypothesis import (
#     test_leadership_hypothesis,
#     test_conflict_hypothesis, 
#     test_group_formation
# )

# def save_dialogue_to_file(dialogue_lines, filename="dialogue_log.txt"):
#     with open(filename, "a", encoding="utf-8") as f:
#         for line in dialogue_lines:
#             f.write(line + "\n")
#     print(f"Диалог сохранён в {filename}")

# def add_imperfections(text, chance=0.3):
#     """Добавляет естественные ошибки в текст"""
#     if random.random() > chance:
#         return text
    
#     # Случайные ошибки пунктуации
#     if random.random() < 0.6:  # 60% шанс на ошибки пунктуации
#         punct_errors = [
#             lambda t: t.replace('.', '').replace('!', '').replace('?', ''),
#             lambda t: t.replace('.', '..').replace('!', '!!'),
#             lambda t: t + random.choice(['..', '!!!', '???', ''])
#         ]
#         text = random.choice(punct_errors)(text)
    
#     # Случайные грамматические ошибки (реже)
#     if random.random() < 0.2:  # 20% шанс на грам. ошибки
#         grammar_errors = [
#             lambda t: t.replace(' что ', ' чо ').replace(' тогда ', ' тада '),
#             lambda t: t.replace(' его ', ' егоно ').replace(' их ', ' ихние '),
#             lambda t: t.replace('ся ', 'сь ').replace('ться ', 'ца ')
#         ]
#         text = random.choice(grammar_errors)(text)
    
#     return text

# def select_tone(speaker_name, responder_name):
#     """Выбор тона ответа"""
#     print(f"\nВыберите тон ответа на реплику {speaker_name}:")
#     for i, (tone, desc) in enumerate(TONE_PROMPTS.items(), 1):
#         print(f"{i}. {tone}: {desc}")
    
#     while True:
#         choice = input("Ваш выбор (1-5 или Enter для случайного): ").strip()
#         if not choice:
#             return random.choice(list(TONE_PROMPTS.keys()))
#         if choice.isdigit() and 1 <= int(choice) <= len(TONE_PROMPTS):
#             return list(TONE_PROMPTS.keys())[int(choice)-1]
#         print("Неверный ввод. Попробуйте снова.")

# def start_dialogue(characters, api_key, model, is_deepseek):
#     """Запускает интерактивный диалог между персонажами"""
#     print("\nДиалог начался! (нажмите 3 для продолжения, 1 для выбора тона, q для выхода)")
    
#     sentiment_analyzer = SentimentAnalyzer()
#     interaction_graph = InteractionGraph()
#     dialogue_history = []
#     dialogue_count = 0

#     # Первая реплика
#     current_speaker = random.choice(list(characters.keys()))
#     first_line = f"{characters[current_speaker]['name']}: {characters[current_speaker]['last_response']}"
#     print(f"\n{first_line}")
#     dialogue_history.append(first_line)
#     save_dialogue_to_file([first_line])

#     while True:
#         user_input = input("\n> ").strip().lower()

#         if user_input == 'q':
#             # Финализируем анализ перед выходом
#             print("\n" + "="*50)
#             print("Финальный анализ социальной динамики:")
#             print("-"*50)
#             print(test_leadership_hypothesis(dialogue_history))
#             print(test_conflict_hypothesis(dialogue_history))
#             print(test_group_formation(dialogue_history))
#             print("="*50)
            
#             graph_file = interaction_graph.visualize()
#             print(f"\nГраф взаимодействий сохранён как {graph_file}")
#             return dialogue_history

#         elif user_input == '1':
#             # Выбираем случайного отвечающего для демонстрации
#             possible_responders = [k for k in characters.keys() if k != current_speaker]
#             responder = random.choice(possible_responders)
#             current_tone = select_tone(
#                 characters[current_speaker]['name'],
#                 characters[responder]['name']
#             )
#             print(f"Выбран тон: {current_tone} для следующего отвечающего")
#             continue

#         elif user_input == '3':
#             spinner = Spinner()
#             spinner.start("Генерирую ответ")
#             dialogue_count += 1

#             # Выбираем нового говорящего
#             next_speaker = random.choice([k for k in characters.keys() if k != current_speaker])
#             next_character = characters[next_speaker]

#             # Формируем промпт с учетом тона
#             tone_prompt = f" (ответь {current_tone.lower()})" if current_tone else ""
#             prompt = f"{characters[current_speaker]['name']} говорит: {characters[current_speaker]['last_response']}\n\n{next_character['name']}, что ответишь?{tone_prompt}"
            
#             # Получаем ответ
#             response = send_request_to_api(
#                 api_key,
#                 model,
#                 prompt,
#                 next_character['prompt'],
#                 is_deepseek
#             )
#             spinner.stop()

#             if response:
#                 # Обработка ответа
#                 clean_response = response.replace(f"{next_character['name']}:", "").strip()
#                 clean_response = add_imperfections(clean_response)
#                 sentiment = sentiment_analyzer.analyze(clean_response) if sentiment_analyzer else "N/A"
                
#                 dialogue_line = f"{next_character['name']}: {clean_response} [Тон: {current_tone or 'обычный'}, Настроение: {sentiment}]"
#                 print(f"\n{dialogue_line}")
#                 dialogue_history.append(dialogue_line)
#                 save_dialogue_to_file([dialogue_line])
                
#                 # Обновляем граф
#                 interaction_graph.add_interaction(
#                     speaker=next_character['name'],
#                     addressee=characters[current_speaker]['name'],
#                     tone=current_tone
#                 )
                
#                 # Обновляем последний ответ
#                 characters[next_speaker]['last_response'] = clean_response
#                 current_speaker = next_speaker
#                 current_tone = None  # Сбрасываем тон после ответа

#                 # Каждые 5 реплик обновляем анализ
#                 if dialogue_count % 5 == 0:
#                     print("\n" + "="*50)
#                     print(f"Анализ после {dialogue_count} реплик:")
#                     print("-"*50)
#                     print(test_leadership_hypothesis(dialogue_history[-5:]))
#                     print(test_conflict_hypothesis(dialogue_history[-5:]))
#                     print(test_group_formation(dialogue_history[-5:]))
#                     print("="*50)
                    
#                     # Обновляем визуализацию графа
#                     temp_graph_file = f"graph_temp_{dialogue_count}.png"
#                     interaction_graph.visualize(temp_graph_file)
#                     print(f"\nОбновленный граф сохранен как {temp_graph_file}")
                    
#                     # Отчет наблюдателя
#                     observer_report = send_request_to_api(
#                         api_key,
#                         model,
#                         prompt=OBSERVER_PROMPT.format(last_dialogues="\n".join(dialogue_history[-5:])),
#                         role_prompt="Ты аналитик социальных отношений.",
#                         is_deepseek=is_deepseek
#                     )
#                     print(f"\nОтчёт наблюдателя:\n{observer_report}\n")
#             else:
#                 print(f"\n{next_character['name']}: *молчит*")

#         else:
#             print("Неверная команда. Нажмите 3 для продолжения, 1 для выбора тона или q для выхода")
            
# def generate_observer_report(api_key, model, is_deepseek, last_dialogues):
#     """Генерирует отчет наблюдателя"""
#     with Spinner("Анализ взаимодействий..."):
#         report = send_request_to_api(
#             api_key, model,
#             prompt=OBSERVER_PROMPT.format(last_dialogues="\n".join(last_dialogues)),
#             role_prompt="Ты опытный психолог, анализирующий групповую динамику.",
#             is_deepseek=is_deepseek
#         )
#         print(f"\n--- Отчет наблюдателя ---\n{report}\n{'='*30}")

import random
import time
from typing import Optional, Dict
from logic.communication import CommunicationManager
from spinner import spinner_context
from analysis.sentiment import SentimentAnalyzer
from analysis.graph import InteractionGraph
from characters.prompts import OBSERVER_PROMPT, TONE_PROMPTS
from analysis.hypothesis import (
    test_leadership_hypothesis,
    test_conflict_hypothesis, 
    test_group_formation
)
from api.client import send_request_to_api

def save_dialogue_to_file(dialogue_lines, filename="dialogue_log.txt"):
    """Сохраняет диалог в файл"""
    with open(filename, "a", encoding="utf-8") as f:
        for line in dialogue_lines:
            f.write(line + "\n")
    print(f"Диалог сохранён в {filename}")

def add_imperfections(text, chance=0.3):
    """Добавляет естественные ошибки в текст"""
    if random.random() > chance:
        return text
    
    if random.random() < 0.6:
        punct_errors = [
            lambda t: t.replace('.', '').replace('!', '').replace('?', ''),
            lambda t: t.replace('.', '..').replace('!', '!!'),
            lambda t: t + random.choice(['..', '!!!', '???', ''])
        ]
        text = random.choice(punct_errors)(text)
    
    if random.random() < 0.2:
        grammar_errors = [
            lambda t: t.replace(' что ', ' чо ').replace(' тогда ', ' тада '),
            lambda t: t.replace(' его ', ' егоно ').replace(' их ', ' ихние '),
            lambda t: t.replace('ся ', 'сь ').replace('ться ', 'ца ')
        ]
        text = random.choice(grammar_errors)(text)
    
    return text

def select_tone(speaker_name, responder_name):
    """Выбор тона ответа"""
    print(f"\nВыберите тон ответа на реплику {speaker_name}:")
    for i, (tone, desc) in enumerate(TONE_PROMPTS.items(), 1):
        print(f"{i}. {tone}: {desc}")
    
    while True:
        choice = input("Ваш выбор (1-5 или Enter для случайного): ").strip()
        if not choice:
            return random.choice(list(TONE_PROMPTS.keys()))
        if choice.isdigit() and 1 <= int(choice) <= len(TONE_PROMPTS):
            return list(TONE_PROMPTS.keys())[int(choice)-1]
        print("Неверный ввод. Попробуйте снова.")

def _generate_public_message(speaker, characters, model, api_key, is_deepseek):
    """Генерация публичного сообщения"""
    prompt = f"{characters[speaker]['name']} говорит вслух всей группе: {characters[speaker]['last_response']}"
    return send_request_to_api(
        api_key,
        model,
        prompt,
        characters[speaker]['prompt'],
        is_deepseek
    )

def _generate_private_message(speaker, listener, characters, model, api_key, is_deepseek):
    """Генерация приватного сообщения"""
    prompt = f"{characters[speaker]['name']} тихо говорит {characters[listener]['name']}: {characters[speaker]['last_response']}"
    return send_request_to_api(
        api_key,
        model,
        prompt,
        characters[speaker]['prompt'],
        is_deepseek
    )

def _select_next_speaker(characters, current_speaker):
    """Выбирает следующего случайного говорящего"""
    available = [name for name in characters.keys() if name != current_speaker]
    if not available:
        return current_speaker
    # Увеличиваем случайность выбора
    weights = [1.0] * len(available)
    return random.choices(available, weights=weights, k=1)[0]

def _process_response(response, speaker, listener, characters, dialogue_history, interaction_graph, sentiment_analyzer, dialogue_type):
    """Обработка сгенерированного ответа"""
    if not response:
        return None
    
    # Очищаем ответ от имени говорящего
    clean_response = response.replace(f"{characters[speaker]['name']}:", "").strip()
    clean_response = add_imperfections(clean_response)
    
    # Анализ тональности
    sentiment_result = sentiment_analyzer.analyze(clean_response)
    sentiment_label = sentiment_result['label']
    sentiment_score = float(sentiment_result['score'])
    
    # Формируем строку диалога
    dialogue_line = f"{characters[speaker]['name']}: {clean_response} [Тип: {dialogue_type}, Настроение: {sentiment_label} ({sentiment_score:.2f})]"
    print(f"\n{dialogue_line}")
    dialogue_history.append(dialogue_line)
    save_dialogue_to_file([dialogue_line])
    
    # Определяем получателя
    target = "ALL" if dialogue_type == "public" else characters[listener]['name']
    
    # Добавляем взаимодействие в граф
    interaction_graph.add_interaction(
        source=characters[speaker]['name'],
        target=target,
        sentiment=sentiment_score,
        comm_type=dialogue_type
    )
    
    # Обновляем последний ответ персонажа
    characters[speaker]['last_response'] = clean_response
    return dialogue_line

def _select_listener(speaker, characters, comm_manager):
    """Выбирает собеседника для частной беседы"""
    available = [name for name in characters 
                if name != speaker and 
                comm_manager.can_start_private(speaker, name)]
    
    if not available:
        return None
    
    # Простые предпочтения по ролям
    role_preferences = {
        "Лидер": ["Умный", "Перфекционист"],
        "Умный": ["Лидер", "Тихоня"],
        "Добрый": ["Тихоня", "Мечтатель"],
        "Шутник": ["Добрый", "Мечтатель"]
    }
    
    # Проверяем предпочтительных собеседников
    for pref in role_preferences.get(speaker, []):
        if pref in available:
            return pref
            
    return random.choice(available)

def _perform_analysis(dialogue_history, interaction_graph, api_key, model, is_deepseek):
    """Выполняет анализ и создает отчет"""
    print("\n" + "="*50)
    print(f"Анализ после {len(dialogue_history)} реплик:")
    print("-"*50)
    print(test_leadership_hypothesis(dialogue_history[-5:]))
    print(test_conflict_hypothesis(dialogue_history[-5:]))
    print(test_group_formation(dialogue_history[-5:]))
    print("="*50)
    
    temp_graph_file = f"graph_temp_{len(dialogue_history)}.png"
    interaction_graph.visualize(temp_graph_file)
    print(f"\nОбновленный граф сохранен как {temp_graph_file}")
    
    with spinner_context("Генерация отчета наблюдателя"):
        observer_report = send_request_to_api(
            api_key,
            model,
            prompt=OBSERVER_PROMPT.format(last_dialogues="\n".join(dialogue_history[-5:])),
            role_prompt="Ты аналитик социальных отношений.",
            is_deepseek=is_deepseek
        )
        print(f"\nОтчёт наблюдателя:\n{observer_report}\n")

def start_dialogue(characters, api_key, model, is_deepseek, environment):
    """Запускает интерактивный диалог между персонажами"""
    print("\nДиалог начался! (нажмите 3 для продолжения, 1 для выбора тона, q для выхода)")
    
    sentiment_analyzer = SentimentAnalyzer()
    interaction_graph = InteractionGraph()
    dialogue_history = []
    dialogue_count = 0
    comm_manager = CommunicationManager(environment)

    # Первая реплика - выбираем случайного персонажа
    current_speaker = random.choice(list(characters.keys()))
    first_line = f"{characters[current_speaker]['name']}: {characters[current_speaker]['last_response']}"
    print(f"\n{first_line}")
    dialogue_history.append(first_line)
    save_dialogue_to_file([first_line])

    while True:
        user_input = input("\n> ").strip().lower()

        if user_input == 'q':
            print("\n" + "="*50)
            print("Финальный анализ социальной динамики:")
            print("-"*50)
            print(test_leadership_hypothesis(dialogue_history))
            print(test_conflict_hypothesis(dialogue_history))
            print(test_group_formation(dialogue_history))
            print("="*50)
            
            graph_file = interaction_graph.visualize()
            print(f"\nГраф взаимодействий сохранён как {graph_file}")
            return dialogue_history

        elif user_input == '1':
            possible_responders = [k for k in characters.keys() if k != current_speaker]
            responder = random.choice(possible_responders)
            current_tone = select_tone(
                characters[current_speaker]['name'],
                characters[responder]['name']
            )
            print(f"Выбран тон: {current_tone} для следующего отвечающего")
            continue

        elif user_input == '3':
            with spinner_context("Генерирую ответ"):
                active_session = comm_manager.get_active_private_session()
                
                if active_session:
                    # Продолжаем текущую приватную беседу
                    speaker = random.choice(active_session)
                    listener = active_session[1] if active_session[0] == speaker else active_session[0]
                    dialogue_type = "private"
                else:
                    # Начинаем новое взаимодействие
                    speaker = current_speaker
                    if comm_manager.can_make_public(speaker) and random.random() < 0.3:
                        dialogue_type = "public"
                    else:
                        dialogue_type = "private"
                        listener = _select_listener(speaker, characters, comm_manager)
                        if not listener:
                            continue
                        comm_manager.start_private_session(speaker, listener)
                
                # Генерация сообщения
                if dialogue_type == "public":
                    response = _generate_public_message(speaker, characters, model, api_key, is_deepseek)
                    comm_manager.last_public[speaker] = time.time()
                else:
                    response = _generate_private_message(speaker, listener, characters, model, api_key, is_deepseek)
                    # Проверка окончания беседы
                    if time.time() > comm_manager.private_sessions[comm_manager._get_session_key(speaker, listener)]:
                        comm_manager.end_private_session(speaker, listener)
                
                # Обработка ответа
                if response:
                    _process_response(
                        response=response,
                        speaker=speaker,
                        listener=listener if dialogue_type == "private" else None,
                        characters=characters,
                        dialogue_history=dialogue_history,
                        interaction_graph=interaction_graph,
                        sentiment_analyzer=sentiment_analyzer,
                        dialogue_type=dialogue_type
                    )
                    
                    if len(dialogue_history) % 5 == 0:
                        _perform_analysis(dialogue_history, interaction_graph, api_key, model, is_deepseek)
                    
                    # Выбираем следующего говорящего
                    next_speaker = _select_next_speaker(characters, speaker)
                    current_speaker = next_speaker
                    current_tone = None
        else:
            print("Неверная команда. Нажмите 3 для продолжения, 1 для выбора тона или q для выхода")