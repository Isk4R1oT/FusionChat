import os
from langchain_core.language_models import LLM
from mistralai import Mistral
from typing import List, Optional, Any
from pydantic import PrivateAttr

class MistralLLM(LLM):
    api_key: str
    model_name: str = "mistral-large-latest"

    _client: Any = PrivateAttr()

    @property
    def _llm_type(self) -> str:
        return "mistral"

    def __init__(self, api_key: str, model_name: str = "mistral-large-latest", **kwargs):
        super().__init__(api_key=api_key, model_name=model_name, **kwargs)
        self._client = Mistral(api_key=api_key)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:

        messages = [{"role": "user", "content": prompt}]

        response = self._client.chat.complete(
            model=self.model_name,
            messages=messages
        )

        if hasattr(response, 'choices') and response.choices and len(response.choices) > 0:
            generated_text = response.choices[0].message.content
        else:
            raise ValueError("Ошибка в ответе от Mistral API")

        if stop:
            for stop_token in stop:
                if stop_token in generated_text:
                    generated_text = generated_text.split(stop_token)[0]

        return generated_text
