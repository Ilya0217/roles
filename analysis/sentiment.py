from typing import Dict, Union
import logging

class SentimentAnalyzer:
    def __init__(self):
        """Инициализация простого анализатора тональности"""
        # Словари для анализа тональности
        self.pos_words = {
            "хорош", "отличн", "прекрасн", "замечательн", "любл", "нрав", 
            "удач", "рад", "давай", "спасибо", "класс", "супер", "крут"
        }
        self.neg_words = {
            "плох", "ужасн", "отвратительн", "ненавиж", "груб", "зл", 
            "разочарован", "злюсь", "нет", "нельзя", "неправильно", "ошибка"
        }
        self.neutral_words = {
            "думаю", "может", "возможно", "наверное", "пожалуй", "вроде"
        }

    def analyze(self, text: str) -> Dict[str, Union[str, float]]:
        """Анализирует тональность текста"""
        text = text.lower()
        words = text.split()
        
        pos_count = sum(1 for word in words if any(pos in word for pos in self.pos_words))
        neg_count = sum(1 for word in words if any(neg in word for neg in self.neg_words))
        neutral_count = sum(1 for word in words if any(neut in word for neut in self.neutral_words))
        
        total = pos_count + neg_count + neutral_count
        if total == 0:
            return {"label": "нейтральный", "score": 0.0}
            
        pos_score = pos_count / total
        neg_score = neg_count / total
        
        if pos_score > neg_score:
            return {"label": "позитивный", "score": pos_score}
        elif neg_score > pos_score:
            return {"label": "негативный", "score": neg_score}
        else:
            return {"label": "нейтральный", "score": 0.5}