def test_leadership_hypothesis(dialogues):
    """Анализирует последние N реплик на лидерские проявления"""
    if not dialogues:
        return "Недостаточно данных для анализа лидерства"
    
    initiators = {}
    for line in dialogues:
        speaker = line.split(":")[0].strip()
        initiators[speaker] = initiators.get(speaker, 0) + 1
    
    leader = max(initiators, key=initiators.get)
    return f"Гипотеза лидерства: {leader} проявил наибольшую активность ({initiators[leader]} инициатив)"

def test_conflict_hypothesis(dialogues):
    """Анализирует последние N реплик на конфликты"""
    conflict_terms = ["конфликт", "спор", "ссора", "раздражен", "злит", "недоволен", "глупость", "ерунда"]
    conflicts = sum(1 for line in dialogues if any(term in line.lower() for term in conflict_terms))
    return f"Гипотеза конфликтов: обнаружено {conflicts} потенциальных конфликтных ситуаций"

def test_group_formation(dialogues):
    """Анализирует последние N реплик на группировки"""
    interactions = {}
    for line in dialogues:
        if "к " in line:
            speaker = line.split(":")[0].strip()
            addressee = line.split("к ")[1].split(" ")[0].strip()
            key = tuple(sorted([speaker, addressee]))
            interactions[key] = interactions.get(key, 0) + 1
    
    if not interactions:
        return "Недостаточно данных для анализа группировок"
    
    top_pair = max(interactions.items(), key=lambda x: x[1])
    return f"Гипотеза группировок: наиболее активная пара - {top_pair[0][0]} и {top_pair[0][1]} ({top_pair[1]} взаимодействий)"
