import os
from langchain_core.language_models import LLM
from mistralai import Mistral
from typing import List, Optional, Any
from pydantic import PrivateAttr

class MistralLLM(LLM):
    # Объявляем поля класса с типами
    api_key: str
    model_name: str = "mistral-large-latest"

    # Клиент API объявляем как приватный атрибут, чтобы он не участвовал в сериализации
    _client: Any = PrivateAttr()

    @property
    def _llm_type(self) -> str:
        return "mistral"

    def __init__(self, api_key: str, model_name: str = "mistral-large-latest", **kwargs):
        # Передаём значения полей в базовый класс
        super().__init__(api_key=api_key, model_name=model_name, **kwargs)
        self._client = Mistral(api_key=api_key)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Основной метод для генерации текста. Принимает строку prompt и возвращает ответ модели.
        """
        # Формируем запрос для API Mistral
        messages = [{"role": "user", "content": prompt}]

        # Используем метод complete, как в рабочем примере
        response = self._client.chat.complete(
            model=self.model_name,
            messages=messages
        )

        # Проверка структуры ответа и извлечение текста
        if hasattr(response, 'choices') and response.choices and len(response.choices) > 0:
            generated_text = response.choices[0].message.content
        else:
            raise ValueError("Ошибка в ответе от Mistral API")

        # Если заданы токены остановки, обрезаем текст до первого вхождения любого из них
        if stop:
            for stop_token in stop:
                if stop_token in generated_text:
                    generated_text = generated_text.split(stop_token)[0]

        return generated_text
