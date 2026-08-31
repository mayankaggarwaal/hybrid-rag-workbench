from abc import ABC, abstractmethod

from google import genai
from google.genai import types
from groq import Groq

SYSTEM_PROMPT = """You are an informational knowledge-support assistant for SYNTHETIC data only.
Use only the supplied evidence. Never invent facts. Every factual claim must cite an
evidence label like [E1]. If evidence is insufficient, say so plainly. Do not infer missing facts."""


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, question: str, evidence: list[str]) -> str: ...


class MockProvider(LLMProvider):
    def generate(self, question: str, evidence: list[str]) -> str:
        if not evidence:
            return "Insufficient evidence is available in this synthetic record to answer the question."
        return "The synthetic record contains the following relevant evidence: " + " ".join(evidence)


class GroqProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self.client, self.model = Groq(api_key=api_key), model

    def generate(self, question: str, evidence: list[str]) -> str:
        prompt = f"Question: {question}\nEvidence:\n" + "\n".join(evidence)
        result = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            temperature=0,
        )
        return result.choices[0].message.content or "Insufficient evidence."


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, question: str, evidence: list[str]) -> str:
        prompt = f"Question: {question}\nEvidence:\n" + "\n".join(evidence)
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0,
            ),
        )
        return response.text or "Insufficient evidence."
