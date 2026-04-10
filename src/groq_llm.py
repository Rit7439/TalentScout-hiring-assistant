"""Groq LLM integration for TalentScout hiring assistant."""

from typing import List, Dict
from groq import Groq


class GroqLLM:
    """Groq-powered language model for interview chatbot.
    
    Uses Groq's cloud inference API — no local model downloads required.
    Free tier supports ~30 requests/min with Llama 3.1 8B.
    """

    def __init__(self, api_key: str, model_name: str = "llama-3.1-8b-instant"):
        """Initialize the Groq client.

        Args:
            api_key: Groq API key from https://console.groq.com/keys
            model_name: Groq model to use (default: llama-3.1-8b-instant)
        """
        self.model_name = model_name
        self.client = Groq(api_key=api_key)

    def generate_response(
        self,
        messages: List[Dict],
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """Generate a response from the conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 - 1.0)

        Returns:
            Generated response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def get_model_info(self) -> Dict:
        """Return metadata about the active model.

        Returns:
            Dictionary with model name and provider info
        """
        return {
            "model_name": self.model_name,
            "provider": "Groq (Cloud Inference)",
            "local_download": False,
        }
