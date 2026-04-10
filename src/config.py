"""Configuration and constants for TalentScout hiring assistant."""

import os
from dotenv import load_dotenv
from typing import Dict, List

# Ensure .env is loaded even if config is imported before streamlit_app calls load_dotenv()
load_dotenv()

def _get_secret(key: str, default: str = "") -> str:
    """Read a secret from environment variables or Streamlit Cloud secrets.
    
    Falls back to st.secrets when running on Streamlit Cloud,
    where secrets are not injected as OS environment variables.
    """
    value = os.getenv(key, "")
    if not value:
        try:
            import streamlit as st
            value = st.secrets.get(key, default)
        except Exception:
            value = default
    return value

# LLM Configuration — Groq Cloud Inference (free tier)
GROQ_API_KEY = _get_secret("GROQ_API_KEY")
# Available models: llama-3.1-8b-instant, llama-3.3-70b-versatile, mixtral-8x7b-32768
GROQ_MODEL = _get_secret("GROQ_MODEL", "llama-3.1-8b-instant")
TEMPERATURE = 0.7
MAX_TOKENS = 512

# Application Configuration
APP_TITLE = "TalentScout - Intelligent Hiring Assistant"
APP_DESCRIPTION = "An AI-powered chatbot for conducting initial candidate interviews"

# Interview Configuration
MAX_QUESTIONS_PER_STACK = 5
MIN_TECH_STACK_ITEMS = 2
CONVERSATION_HISTORY_LIMIT = 50

# Supported Programming Languages and Frameworks
TECH_STACK_KEYWORDS = {
    "backend": {
        "languages": ["python", "java", "javascript", "typescript", "go", "rust", "c#", "php", "ruby"],
        "frameworks": ["django", "flask", "fastapi", "spring", "express", "node.js", "asp.net", "rails"]
    },
    "frontend": {
        "languages": ["javascript", "typescript", "html", "css", "jsx", "tsx"],
        "frameworks": ["react", "vue", "angular", "svelte", "next.js", "nuxt", "gatsby"]
    },
    "databases": ["postgresql", "mysql", "mongodb", "redis", "firebase", "elasticsearch", "dynamodb"],
    "cloud": ["aws", "gcp", "azure", "heroku", "vercel", "netlify"],
    "tools": ["git", "docker", "kubernetes", "jenkins", "gitlab-ci", "github-actions"]
}

# Conversation Flow
INITIAL_GREETING = """
Hello! 👋 Welcome to TalentScout, your AI-powered hiring assistant. 

I'm here to get to know you better and understand your professional background. Let's start with some basic information:

1. What's your full name?
2. What's your contact (email or phone)?
3. How many years of experience do you have?
4. What positions are you interested in?

Feel free to share as much detail as you'd like!
"""

# Data Privacy
DATA_PRIVACY_NOTICE = """
📋 **Data Privacy Notice**: All your information will be handled securely and used only for evaluation purposes, in compliance with GDPR and data protection standards.
"""

# Question Categories
QUESTION_CATEGORIES = {
    "conceptual": "Explain key concepts and fundamentals",
    "practical": "Real-world implementation and problem-solving",
    "architectural": "System design and architecture decisions",
    "debugging": "Troubleshooting and debugging scenarios",
    "optimization": "Performance and optimization techniques"
}
