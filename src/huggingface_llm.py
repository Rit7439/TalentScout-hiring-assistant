"""HuggingFace LLM integration for TalentScout."""

from typing import List, Dict, Optional
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM


class HuggingFaceLLM:
    """HuggingFace language model for interview chatbot."""
    
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"):
        """Initialize HuggingFace model.
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading model: {model_name}")
        print(f"Using device: {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto"
            )
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def generate_response(
        self,
        messages: List[Dict],
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """Generate response from conversation history.
        
        Args:
            messages: Conversation history with role and content
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated response text
        """
        # Format messages into prompt
        prompt = self._format_messages(messages)
        
        try:
            outputs = self.pipeline(
                prompt,
                max_length=max_tokens + len(self.tokenizer.encode(prompt)),
                temperature=temperature,
                top_p=0.95,
                do_sample=True,
                return_full_text=False
            )
            
            response = outputs[0]["generated_text"].strip()
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _format_messages(self, messages: List[Dict]) -> str:
        """Format messages into prompt for the model.
        
        Args:
            messages: List of message dicts with role and content
            
        Returns:
            Formatted prompt string
        """
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            
            if role == "SYSTEM":
                prompt += f"System: {content}\n\n"
            elif role == "USER":
                prompt += f"User: {content}\n"
            elif role == "ASSISTANT":
                prompt += f"Assistant: {content}\n"
        
        prompt += "Assistant: "
        return prompt
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "model_size": self._get_model_size(),
            "supports_gpu": torch.cuda.is_available()
        }
    
    def _get_model_size(self) -> str:
        """Get model size in GB.
        
        Returns:
            Model size as string
        """
        total_params = sum(p.numel() for p in self.model.parameters())
        gb = total_params * 4 / 1024 / 1024 / 1024  # Approximate for float32
        return f"{gb:.2f}B params"
