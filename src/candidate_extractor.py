"""Extract candidate information from conversation messages."""

import re
from typing import Dict, List, Set, Optional
from src.config import TECH_STACK_KEYWORDS


class CandidateExtractor:
    """Extracts structured candidate information from conversation."""
    
    def __init__(self):
        self.name: Optional[str] = None
        self.contact: Optional[str] = None
        self.experience_years: Optional[int] = None
        self.positions_interested: List[str] = []
        self.detected_tech_stack: Set[str] = set()
        self.education: Optional[str] = None
        self.location: Optional[str] = None
        self.current_role: Optional[str] = None
        
    def extract_from_message(self, message: str) -> None:
        """Extract candidate information from a single message."""
        message_lower = message.lower()

        # Extract name — patterns: "my name is X", "I am X", "I'm X", "this is X"
        if not self.name:
            name_patterns = [
                r"(?:my name is|i am|i'm|this is|call me)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
                r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)$",  # Standalone capitalized name on its own line
            ]
            for pattern in name_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    candidate_name = match.group(1).strip()
                    # Filter out common false positives
                    excluded = {"backend", "frontend", "python", "java", "html", "css"}
                    if candidate_name.lower() not in excluded and len(candidate_name) > 1:
                        self.name = candidate_name
                        break

        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        if emails and not self.contact:
            self.contact = emails[0]

        # Extract phone number
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        phones = re.findall(phone_pattern, message)
        if phones and not self.contact:
            self.contact = ''.join(phones[0])

        # Extract years of experience — handles "5 years", "5 yrs", "5 years of experience"
        exp_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience\s*(?:of\s*)?)(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*(?:in\s*the\s*field)?',
        ]
        if not self.experience_years:
            for pattern in exp_patterns:
                exp_match = re.search(pattern, message_lower)
                if exp_match:
                    self.experience_years = int(exp_match.group(1))
                    break

        # Extract location
        if not self.location:
            loc_match = re.search(
                r'(?:based in|located in|from|living in|i am in|i\'m in)\s+([A-Za-z\s,]+?)(?:\.|,|$)',
                message, re.IGNORECASE
            )
            if loc_match:
                self.location = loc_match.group(1).strip()

        # Extract current role
        if not self.current_role:
            role_match = re.search(
                r'(?:currently\s+(?:working\s+as|a)|i am\s+a|i\'m\s+a|working as\s+a?)\s+([A-Za-z\s]+?)(?:\s+at|\.|,|$)',
                message, re.IGNORECASE
            )
            if role_match:
                self.current_role = role_match.group(1).strip()

        # Detect tech stack
        self._detect_tech_stack(message_lower)

        # Extract positions interested
        positions = ["frontend", "backend", "full stack", "devops", "data engineer",
                     "ml engineer", "qa engineer", "mobile", "android", "ios"]
        for pos in positions:
            if pos in message_lower and pos not in self.positions_interested:
                self.positions_interested.append(pos)
    
    def _detect_tech_stack(self, message_lower: str) -> None:
        """Detect technologies mentioned in message."""
        # Check all keywords
        all_keywords = []
        for category in TECH_STACK_KEYWORDS.values():
            if isinstance(category, dict):
                for sublist in category.values():
                    all_keywords.extend(sublist)
            else:
                all_keywords.extend(category)
        
        for keyword in all_keywords:
            if keyword in message_lower:
                self.detected_tech_stack.add(keyword)
    
    def get_tech_stack(self) -> List[str]:
        """Return detected tech stack as list."""
        return sorted(list(self.detected_tech_stack))
    
    def get_summary(self) -> Dict:
        """Return extracted candidate information as dictionary."""
        return {
            "name": self.name,
            "contact": self.contact,
            "experience_years": self.experience_years,
            "positions_interested": self.positions_interested,
            "tech_stack": self.get_tech_stack(),
            "education": self.education,
            "location": self.location,
            "current_role": self.current_role
        }
