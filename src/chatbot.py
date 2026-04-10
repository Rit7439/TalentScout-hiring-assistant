"""Core chatbot logic for TalentScout hiring assistant."""

import os
from typing import List, Dict, Optional
from src.config import GROQ_API_KEY, GROQ_MODEL, TEMPERATURE, MAX_TOKENS, INITIAL_GREETING
from src.groq_llm import GroqLLM
from src.prompt_engine import PromptEngine
from src.candidate_extractor import CandidateExtractor
from src.data_handler import DataHandler


class TalentScoutChatbot:
    """Main chatbot class for conducting hiring interviews via Groq."""

    def __init__(self):
        """Initialize the chatbot with Groq LLM."""
        if not GROQ_API_KEY:
            raise ValueError(
                "Groq API key not found. Please set the GROQ_API_KEY environment variable. "
                "Get a free key at: https://console.groq.com/keys"
            )

        self.llm = GroqLLM(api_key=GROQ_API_KEY, model_name=GROQ_MODEL)
        self.conversation_history: List[Dict] = []
        self.candidate_extractor = CandidateExtractor()
        self.data_handler = DataHandler()
        self.system_prompt = PromptEngine.get_system_prompt()
        self.candidate_id: Optional[str] = None
        self.interview_stage = "greeting"  # greeting, info_gathering, tech_questions, closing

    def start_interview(self) -> str:
        """Start a new interview and return greeting."""
        self.interview_stage = "greeting"
        self.conversation_history = []
        greeting = INITIAL_GREETING
        self._add_to_history("assistant", greeting)
        return greeting

    def process_message(self, user_message: str) -> str:
        """Process user message and return assistant response."""
        # Extract candidate info from user message
        self.candidate_extractor.extract_from_message(user_message)
        self._add_to_history("user", user_message)

        # Generate response from Groq
        response = self._get_ai_response()
        self._add_to_history("assistant", response)

        # Update interview stage based on collected info
        self._update_interview_stage()

        return response

    def generate_technical_questions(self) -> str:
        """Generate technical questions based on candidate's tech stack."""
        tech_stack = self.candidate_extractor.get_tech_stack()
        experience_years = self.candidate_extractor.experience_years or 0
        position = ", ".join(self.candidate_extractor.positions_interested) or "General"

        if not tech_stack:
            return "I need more information about your technical skills. Could you mention some technologies or frameworks you've worked with?"

        experience_level = PromptEngine.get_experience_level(experience_years)

        prompt = PromptEngine.generate_tech_questions_prompt(
            tech_stack=tech_stack,
            experience_level=experience_level,
            position=position
        )

        # Use Groq to generate questions
        response = self.llm.generate_response(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        return response

    def get_candidate_summary(self) -> Dict:
        """Get candidate information summary."""
        return self.candidate_extractor.get_summary()

    def finalize_interview(self) -> str:
        """End interview and provide summary."""
        self.interview_stage = "closing"
        summary = self.get_candidate_summary()

        # Save candidate data
        if summary.get("name") or summary.get("contact"):
            self.candidate_id = self.data_handler.save_candidate(summary)
            self.data_handler.save_conversation(self.candidate_id, self.conversation_history)

        closing_message = f"""
Thank you so much for this great conversation! Here's a summary of what we discussed:

**Your Profile:**
- Experience: {summary.get('experience_years', 'N/A')} years
- Technical Stack: {', '.join(summary.get('tech_stack', [])) or 'Not specified'}
- Positions Interested: {', '.join(summary.get('positions_interested', [])) or 'Not specified'}

**Next Steps:**
We'll review your information and get back to you within 48 hours. In the meantime, feel free to check our website or reach out if you have any questions.

Looking forward to the next stage! 🚀
"""
        self._add_to_history("assistant", closing_message)
        return closing_message

    def _get_ai_response(self) -> str:
        """Get response from Groq LLM."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history
        ]
        return self.llm.generate_response(
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

    def _add_to_history(self, role: str, content: str) -> None:
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def _update_interview_stage(self) -> None:
        """Update interview stage based on collected information."""
        summary = self.get_candidate_summary()

        if self.interview_stage == "greeting":
            if summary.get("name") and summary.get("contact"):
                self.interview_stage = "info_gathering"

        elif self.interview_stage == "info_gathering":
            if (
                summary.get("experience_years") is not None
                and summary.get("tech_stack")
                and len(self.conversation_history) > 6
            ):
                self.interview_stage = "tech_questions"

    def get_conversation_history(self) -> List[Dict]:
        """Return conversation history."""
        return self.conversation_history

    def export_interview_data(self) -> Optional[str]:
        """Export interview data and return candidate ID.
        
        Auto-saves candidate data if finalize_interview() was not called yet.
        """
        if self.candidate_id:
            # Already saved — just return existing ID
            return self.candidate_id

        # Not yet saved — save now using whatever data was collected so far
        summary = self.get_candidate_summary()
        if summary.get("name") or summary.get("contact") or summary.get("tech_stack"):
            self.candidate_id = self.data_handler.save_candidate(summary)
            self.data_handler.save_conversation(self.candidate_id, self.conversation_history)
            return self.candidate_id

        return None
