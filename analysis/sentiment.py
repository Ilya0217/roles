from typing import Dict, Union
import logging
from transformers import pipeline
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        """Инициализация анализатора тональности с резервным упрощенным режимом"""
        self.analyzer = None
        self._init_advanced_analyzer()
        
        # Словари для упрощенного анализа
        self.pos_words = {"хорош", "отличн", "прекрасн", "замечательн", "любл", "нрав", "удач", "рад"}
        self.neg_words = {"плох", "ужасн", "отвратительн", "ненавиж", "груб", "зл", "разочарован", "злюсь"}
        self.weights = {
            'позитивный': 0.7,
            'нейтральный': 0.1,
            'негативный': -0.7
        }

    def _init_advanced_analyzer(self):
        """Инициализация продвинутого анализатора"""
        try:
            self.analyzer = pipeline(
                "text-classification",
                model="blanchefort/rubert-base-cased-sentiment",
                framework="pt",
                device="cpu"
            )
        except Exception as e:
            logging.warning(f"Не удалось инициализировать анализатор: {str(e)}")
            self.analyzer = None

    def analyze(self, text: str) -> Dict[str, Union[str, float]]:
        """
        Анализирует тональность текста
        Возвращает словарь с меткой и оценкой
        """
        if not text:
            return {"label": "нейтральный", "score": 0.0}
            
        if self.analyzer:
            try:
                result = self.analyzer(text)[0]
                return {
                    "label": self._translate_label(result['label']),
                    "score": float(result['score']) * self._get_weight(result['label'])
                }
            except Exception as e:
                logging.error(f"Ошибка анализа: {str(e)}")
                
        # Упрощенный анализ как резервный вариант
        return self._simple_analyze(text)

    def _translate_label(self, label: str) -> str:
        """Переводит метки на русский"""
        label_map = {
            "POSITIVE": "позитивный",
            "NEUTRAL": "нейтральный",
            "NEGATIVE": "негативный"
        }
        return label_map.get(label, label)

    def _get_weight(self, label: str) -> float:
        """Возвращает весовой коэффициент для метки"""
        return self.weights.get(self._translate_label(label), 0.1)

    def _simple_analyze(self, text: str) -> Dict[str, Union[str, float]]:
        """Упрощенный анализ тональности"""
        text_lower = text.lower()
        pos = sum(1 for w in self.pos_words if w in text_lower)
        neg = sum(1 for w in self.neg_words if w in text_lower)
        
        if pos > neg:
            return {"label": "позитивный", "score": min(0.5 + pos*0.1, 1.0)}
        elif neg > pos:
            return {"label": "негативный", "score": max(-0.5 - neg*0.1, -1.0)}
        return {"label": "нейтральный", "score": 0.0}