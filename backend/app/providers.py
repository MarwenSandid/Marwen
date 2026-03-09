from __future__ import annotations

import base64
import json
import os
from abc import ABC, abstractmethod

from openai import OpenAI

from .schemas import CarAnalysis


class VisionProvider(ABC):
    @abstractmethod
    def analyze(self, image_bytes: bytes) -> CarAnalysis:
        raise NotImplementedError


class MockVisionProvider(VisionProvider):
    def analyze(self, image_bytes: bytes) -> CarAnalysis:
        return CarAnalysis(
            make="unknown",
            model="unknown",
            production_date="unknown",
            country_of_origin="unknown",
            confidence=0.0,
            notes="Mock response. Set OPENAI_API_KEY for real model inference.",
        )


class OpenAIVisionProvider(VisionProvider):
    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model

    def analyze(self, image_bytes: bytes) -> CarAnalysis:
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are a vehicle recognition assistant. Return JSON with keys: "
                                "make, model, production_date, country_of_origin, confidence, notes. "
                                "If uncertain use 'unknown'. confidence is 0 to 1."
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        }
                    ],
                },
            ],
        )
        output_text = response.output_text
        data = json.loads(output_text)
        return CarAnalysis(**data)


def build_provider() -> VisionProvider:
    if os.environ.get("OPENAI_API_KEY"):
        return OpenAIVisionProvider()
    return MockVisionProvider()
