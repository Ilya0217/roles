from typing import Dict, List, Tuple, Optional
import time
import random
from characters.prompts import ENVIRONMENT_PROMPTS

class CommunicationManager:
    def __init__(self, environment: str):
        self.environment = environment
        env_config = ENVIRONMENT_PROMPTS[environment]
        
        # Настройка параметров в зависимости от окружения
        if environment == "school":
            self.public_cooldown = 300  # 5 минут между публичными высказываниями
            self.private_duration = 180  # 3 минуты на частную беседу
            self.private_timeout = 600  # 10 минут таймаут между частными беседами
        else:  # emergency
            self.public_cooldown = 60   # 1 минута между публичными высказываниями
            self.private_duration = 30  # 30 секунд на частную беседу
            self.private_timeout = 120  # 2 минуты таймаут между частными беседами
            
        self.last_public: Dict[str, float] = {}
        self.private_sessions: Dict[Tuple[str, str], float] = {}
        self.private_timeouts: Dict[Tuple[str, str], float] = {}

    def can_start_private(self, speaker: str, listener: str) -> bool:
        """Проверяет возможность начать частный диалог"""
        key = self._get_session_key(speaker, listener)
        return (key not in self.private_timeouts or 
                self.private_timeouts[key] < time.time())

    def can_make_public(self, speaker: str) -> bool:
        """Проверяет возможность публичного высказывания"""
        return (speaker not in self.last_public or 
                self.last_public[speaker] + self.public_cooldown < time.time())

    def start_private_session(self, speaker: str, listener: str):
        """Начинает новую частную беседу"""
        key = self._get_session_key(speaker, listener)
        self.private_sessions[key] = time.time() + self.private_duration

    def end_private_session(self, speaker: str, listener: str):
        """Завершает частную беседу и устанавливает таймаут"""
        key = self._get_session_key(speaker, listener)
        if key in self.private_sessions:
            del self.private_sessions[key]
        self.private_timeouts[key] = time.time() + self.private_timeout

    def get_active_private_session(self) -> Optional[Tuple[str, str]]:
        """Возвращает текущую активную частную беседу"""
        for (a, b), end_time in self.private_sessions.items():
            if end_time > time.time():
                return (a, b)
        return None

    def _get_session_key(self, a: str, b: str) -> Tuple[str, str]:
        """Упорядоченный ключ для сессии"""
        return tuple(sorted([a, b]))