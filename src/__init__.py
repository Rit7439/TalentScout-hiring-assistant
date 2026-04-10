"""TalentScout - Intelligent Hiring Assistant Package."""

from src.chatbot import TalentScoutChatbot
from src.candidate_extractor import CandidateExtractor
from src.prompt_engine import PromptEngine
from src.data_handler import DataHandler

__version__ = "1.0.0"
__author__ = "TalentScout Team"

__all__ = [
    "TalentScoutChatbot",
    "CandidateExtractor",
    "PromptEngine",
    "DataHandler"
]
