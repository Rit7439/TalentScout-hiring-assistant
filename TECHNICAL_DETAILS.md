# TalentScout — Technical Details & Architecture

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                        │
│   (Chat Interface, Sidebar Controls, Data Export Preview)    │
└─────────────────────┬────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────────┐
│              TalentScoutChatbot  (chatbot.py)                 │
│   Interview orchestration, session state, stage management   │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │CandidateExtract │  │PromptEngine  │  │  DataHandler   │  │
│  │(regex + NLP)    │  │(templates)   │  │(JSON + GDPR)   │  │
│  └─────────────────┘  └──────────────┘  └────────────────┘  │
└─────────────────────┬────────────────────────────────────────┘
                      │
             ┌────────▼────────┐
             │   GroqLLM        │
             │  (groq_llm.py)  │
             └────────┬────────┘
                      │ HTTPS API call
             ┌────────▼────────┐
             │   Groq Cloud     │
             │ Llama 3.1 8B    │
             └─────────────────┘
```

---

## Core Modules

### 1. `chatbot.py` — TalentScoutChatbot
Main orchestrator for the full interview lifecycle.

**Key Methods:**
```python
start_interview()               # Reset state, return greeting message
process_message(user_message)   # Extract info + get LLM response
generate_technical_questions()  # Build prompt, call Groq, return questions
finalize_interview()            # Save data, return closing message
export_interview_data()         # Auto-save + return candidate ID
get_candidate_summary()         # Return extracted candidate profile dict
```

**Interview Stages:**
| Stage | Trigger | Description |
|---|---|---|
| `greeting` | Start | Welcome candidate, ask for name + contact |
| `info_gathering` | Name + contact collected | Ask about experience and tech stack |
| `tech_questions` | Tech stack + 6+ messages | Ask technical questions |
| `closing` | Finalize button | Summarize and save |

---

### 2. `groq_llm.py` — GroqLLM
Thin wrapper around the Groq Python SDK.

**Why Groq instead of HuggingFace?**
- HuggingFace Mistral-7B requires ~14GB download and GPU/high-RAM machine
- Groq runs inference on custom LPU hardware — responses in < 1 second
- Free tier: ~30 req/min, no credit card required

**API call pattern:**
```python
client = Groq(api_key=GROQ_API_KEY)
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": "..."},
        {"role": "assistant", "content": "..."},
    ],
    temperature=0.7,
    max_tokens=512
)
```

**Available Models:**
| Model | Speed | Capability | Context |
|---|---|---|---|
| `llama-3.1-8b-instant` | ⚡⚡⚡ Fastest | Good | 128K |
| `llama-3.3-70b-versatile` | ⚡⚡ Fast | Best | 128K |
| `mixtral-8x7b-32768` | ⚡ Moderate | Good | 32K |

---

### 3. `candidate_extractor.py` — CandidateExtractor
Extracts structured data from free-form conversational text using regex and keyword matching.

**Extraction Methods:**
| Field | Technique | Example Input |
|---|---|---|
| Name | Regex: `"my name is X"`, `"I am X"`, `"I'm X"` | `"My name is Rahul Das"` |
| Email | RFC-compliant regex | `"reach me at r@example.com"` |
| Phone | 10-digit pattern | `"call me at 9876543210"` |
| Experience | Number + years/yrs pattern | `"5 years of experience"` |
| Tech stack | Keyword DB matching (50+ terms) | `"I use Python and FastAPI"` |
| Position | Fixed keyword list | `"interested in backend roles"` |
| Location | `"based in / from / living in"` | `"based in Mumbai"` |
| Current role | `"working as / I'm a"` | `"I'm a software engineer"` |

**Tech Stack Detection Coverage:**
```python
TECH_STACK_KEYWORDS = {
    "backend":   { languages: [...], frameworks: [...] },
    "frontend":  { languages: [...], frameworks: [...] },
    "databases": [...],
    "cloud":     [...],
    "tools":     [...]
}
```
50+ keywords across Python, Java, Go, Rust, JS/TS, React, Vue, Angular,
Django, FastAPI, Flask, Spring, Express, PostgreSQL, MySQL, MongoDB, Redis,
AWS, GCP, Azure, Docker, Kubernetes, Git, and more.

---

### 4. `prompt_engine.py` — PromptEngine
All AI prompt templates live here. Centralizing prompts makes iteration fast and keeps concerns separated.

**Prompt Types:**

| Prompt | Purpose |
|---|---|
| `SYSTEM_PROMPT` | Defines the TalentScout persona, required data fields, question strategy, and GDPR behavior |
| `TECH_QUESTION_PROMPT_TEMPLATE` | Generates 3–5 technical questions from tech stack + experience level + position |
| `FOLLOW_UP_PROMPT_TEMPLATE` | Generates context-aware follow-up question from previous answer |
| `EVALUATION_SUMMARY_PROMPT` | Produces structured candidate evaluation summary |

**Prompt Design Principles:**
1. **Specificity**: Every prompt names the exact output format expected
2. **Adaptability**: `{experience_level}` variable adjusts question difficulty dynamically
3. **Coverage**: Prompt explicitly lists 20+ technology categories to handle diverse stacks
4. **One-at-a-time**: System prompt instructs the model to ask one question per message
5. **Privacy-aware**: System prompt includes GDPR handling instructions

**Experience Level Mapping:**
```python
< 2 years  → "Junior"
2–5 years  → "Mid-level"
5–10 years → "Senior"
10+ years  → "Expert"
```

---

### 5. `data_handler.py` — DataHandler
Manages all data persistence and privacy operations.

**Storage Structure:**

`data/candidates.json`:
```json
{
  "cand_20260410_133143": {
    "id": "cand_20260410_133143",
    "name": "Rahul Das",
    "contact": "rdas88839@gmail.com",
    "experience_years": 1,
    "tech_stack": ["css", "fastapi", "git", "html", "python"],
    "positions_interested": ["backend"],
    "education": null,
    "location": null,
    "current_role": null,
    "created_at": "2026-04-10T13:31:43.777250"
  }
}
```

`data/conversations.json`:
```json
{
  "cand_20260410_133143": {
    "messages": [
      {"role": "assistant", "content": "Hello! Welcome to TalentScout..."},
      {"role": "user", "content": "Hi, my name is Rahul..."}
    ],
    "updated_at": "2026-04-10T13:31:43.777250"
  }
}
```

**GDPR Methods:**
```python
anonymize_candidate_data(data)  # Removes name, contact, location
export_candidate_summary(id)    # Returns full profile + message count
```

---

### 6. `config.py` — Configuration
Single source of truth for all constants and settings.

**Key Settings:**
```python
GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL    = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
TEMPERATURE   = 0.7    # Balance between consistency and creativity
MAX_TOKENS    = 512    # Sufficient for structured interview responses
```

---

## Data Flow

```
User types message
       ↓
streamlit_app.py receives input
       ↓
TalentScoutChatbot.process_message()
       ├── CandidateExtractor.extract_from_message()   ← regex parsing
       ├── Appends to conversation_history
       └── GroqLLM.generate_response(history)
              ↓ HTTPS request
           Groq Cloud (Llama 3.1 8B)
              ↓ JSON response
       LLM response returned → displayed in chat
       ↓
On Export/Finalize:
       └── DataHandler.save_candidate() → candidates.json
       └── DataHandler.save_conversation() → conversations.json
```

---

## Libraries & Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | Latest | Web UI framework |
| `groq` | 1.1.2+ | Groq cloud LLM inference client |
| `python-dotenv` | Latest | Load `.env` environment variables |

No `torch`, `transformers`, or heavy ML libraries required.

---

## Data Privacy & Security

### GDPR Compliance Checklist
- ✅ **Purpose limitation**: Only recruitment-necessary data collected
- ✅ **Data minimization**: Optional fields (location, role) are nullable
- ✅ **Transparency**: Privacy notice displayed to every candidate
- ✅ **Right of access**: Export button provides full data
- ✅ **Anonymization**: `anonymize_candidate_data()` removes all PII
- ✅ **Storage security**: Data files excluded from version control
- ✅ **API key safety**: `.env` gitignored, never hardcoded

---

## Performance

| Operation | Typical Time |
|---|---|
| First message response | < 1 second |
| Technical question generation | 1–2 seconds |
| Data export/save | < 100ms |
| App startup | 2–3 seconds |

---

## Deployment Options

### Local
```bash
venv\Scripts\streamlit run streamlit_app.py
```

### Streamlit Cloud (Free)
1. Push to GitHub (`.env` is gitignored)
2. Add `GROQ_API_KEY` in Streamlit Cloud → App Settings → Secrets
3. Auto-deploys on every push

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### AWS ECS / GCP Cloud Run
Build the Docker image and deploy to any container platform.
Pass `GROQ_API_KEY` as an environment variable in the container config.

---

**Last Updated**: April 10, 2026
**Version**: 1.1.0
**LLM**: Groq — Llama 3.1 8B Instant (free tier)
