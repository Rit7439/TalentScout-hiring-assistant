"""Prompt engineering and question generation for technical interviews."""

from typing import List, Dict
from src.config import QUESTION_CATEGORIES


class PromptEngine:
    """Manages prompt templates and generates technical questions."""
    
    SYSTEM_PROMPT = """You are TalentScout, an intelligent and empathetic hiring assistant for technical recruitment.

Your PRIMARY responsibilities during the interview:

1. **Information Gathering** (collect ALL of the following):
   - Full name (ask clearly if not provided)
   - Contact details (email or phone)
   - Years of professional experience
   - Desired position(s) (e.g. backend, frontend, full stack, DevOps, ML engineer)
   - Tech stack: programming languages, frameworks, databases, cloud tools, DevOps tools
   - Current/previous role and location (optional but helpful)

2. **Technical Assessment**:
   - Ask 3-5 technical questions tailored to the candidate's declared tech stack
   - Adapt difficulty based on experience level (junior/mid/senior/expert)
   - Cover conceptual understanding, practical implementation, and problem-solving
   - Support diverse stacks: Python, Java, JavaScript/TypeScript, Go, Rust, React, Angular, Vue,
     Django, FastAPI, Spring, Node.js, PostgreSQL, MongoDB, Redis, AWS, GCP, Azure, Docker, Kubernetes

3. **Conversation Guidelines**:
   - Be professional, warm, and encouraging
   - Ask ONE question at a time — do not overwhelm the candidate
   - If a field is missing, naturally ask for it in context
   - Acknowledge candidate responses before asking the next question
   - Never ask for sensitive info beyond what's needed for recruitment

4. **Data Privacy**:
   - Treat all personal information with strict confidentiality
   - Only collect what is necessary for the evaluation
   - Inform the candidate their data is handled per GDPR standards

5. **Closing**:
   - Thank the candidate warmly
   - Summarize what was covered
   - Outline next steps clearly"""

    TECH_QUESTION_PROMPT_TEMPLATE = """Based on the candidate's tech stack: {tech_stack}

Generate 3-5 relevant technical interview questions that assess:
- Conceptual understanding
- Practical implementation experience
- Problem-solving abilities
- Real-world applications

Format each question with:
1. Question text
2. What we're assessing
3. Ideal answer points

Tech Stack: {tech_stack}
Experience Level: {experience_level}
Position: {position}

Make questions progressively challenging."""

    FOLLOW_UP_PROMPT_TEMPLATE = """Based on the candidate's previous answer about {topic}, generate a thoughtful follow-up question that:
- Digs deeper into their understanding
- Explores edge cases or advanced concepts
- Tests problem-solving approach
- Maintains conversation flow

Candidate's Experience: {experience_years} years
Tech Stack Focus: {tech_stack}

Keep the question natural and conversational."""

    EVALUATION_SUMMARY_PROMPT = """Summarize the candidate interview with:
1. Key strengths identified
2. Areas for development
3. Cultural fit assessment
4. Recommendation for next round
5. Notable achievements mentioned

Candidate Info:
- Name: {name}
- Experience: {experience_years} years
- Tech Stack: {tech_stack}

Interview Summary:
{conversation_summary}"""

    @staticmethod
    def get_system_prompt() -> str:
        """Return the system prompt for the chatbot."""
        return PromptEngine.SYSTEM_PROMPT
    
    @staticmethod
    def generate_tech_questions_prompt(
        tech_stack: List[str],
        experience_level: str,
        position: str
    ) -> str:
        """Generate a prompt for technical questions."""
        return PromptEngine.TECH_QUESTION_PROMPT_TEMPLATE.format(
            tech_stack=", ".join(tech_stack),
            experience_level=experience_level,
            position=position
        )
    
    @staticmethod
    def generate_follow_up_prompt(
        topic: str,
        experience_years: int,
        tech_stack: List[str]
    ) -> str:
        """Generate a follow-up question prompt."""
        return PromptEngine.FOLLOW_UP_PROMPT_TEMPLATE.format(
            topic=topic,
            experience_years=experience_years,
            tech_stack=", ".join(tech_stack)
        )
    
    @staticmethod
    def generate_evaluation_prompt(
        name: str,
        experience_years: int,
        tech_stack: List[str],
        conversation_summary: str
    ) -> str:
        """Generate an evaluation summary prompt."""
        return PromptEngine.EVALUATION_SUMMARY_PROMPT.format(
            name=name,
            experience_years=experience_years,
            tech_stack=", ".join(tech_stack),
            conversation_summary=conversation_summary
        )
    
    @staticmethod
    def get_experience_level(years: int) -> str:
        """Determine experience level from years."""
        if years < 2:
            return "Junior"
        elif years < 5:
            return "Mid-level"
        elif years < 10:
            return "Senior"
        else:
            return "Expert"
    
    @staticmethod
    def format_conversation_for_evaluation(messages: List[Dict]) -> str:
        """Format conversation history for evaluation."""
        formatted = []
        for msg in messages:
            role = msg.get("role", "").upper()
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}\n")
        return "".join(formatted)
