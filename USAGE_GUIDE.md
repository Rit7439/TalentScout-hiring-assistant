# TalentScout - Usage Guide

Complete step-by-step instructions for using the TalentScout hiring assistant.

## Table of Contents
1. [Getting Started](#getting-started)
2. [First Interview Setup](#first-interview-setup)
3. [During the Interview](#during-the-interview)
4. [Advanced Features](#advanced-features)
5. [Troubleshooting](#troubleshooting)
6. [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### Prerequisites
- Python 3.8 or higher installed
- OpenAI API key (from platform.openai.com)
- Internet connection

### Installation Steps

#### Step 1: Navigate to Project Directory
```bash
cd "C:\Users\WINDOWS\OneDrive\Desktop\TalentScout HIRING"
```

#### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Setup Environment Configuration
Create a `.env` file in the project root directory:
```bash
OPENAI_API_KEY=sk-your_actual_api_key_here
```

**To get your API key:**
1. Visit https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the key (visible only once)
4. Paste into `.env` file

### Verify Installation
```bash
python -c "import streamlit; print('Streamlit installed!')"
python -c "import openai; print('OpenAI installed!')"
```

---

## First Interview Setup

### Launching the Application

```bash
streamlit run streamlit_app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://your.ip.address:8501
```

Your browser should automatically open. If not, visit `http://localhost:8501`

### Application Interface Overview

```
┌─────────────────────────────────────────────────────┐
│         🤖 TalentScout - Hiring Assistant          │
│    AI-powered intelligent candidate interviewer    │
├─────────────┬───────────────────────────────────────┤
│             │  Main Chat Area                       │
│   LEFT      │  - Welcome message                    │
│   SIDEBAR   │  - Message exchange                   │
│             │  - Real-time responses                │
│   📋        │                                       │
│   Controls  │                                       │
│   📊        │                                       │
│   Summary   │                                       │
│             │                                       │
└─────────────┴───────────────────────────────────────┘
```

### Sidebar Controls Explained

**📋 Interview Controls Section:**
- **🚀 Start New Interview**: Begin a fresh interview session
- Shows candidate summary as information is collected
- Displays detected tech stack
- Shows interested positions

**Data Privacy Notice:**
- GDPR compliance information
- Data handling practices

**Helpful Tips:**
- Information is processed in real-time
- Tech stack is detected automatically
- No manual input of technologies needed

---

## During the Interview

### Step 1: Begin Interview

1. Click **Begin Interview** button in the main area
2. Read the greeting from the chatbot
3. Chatbot introduces itself and asks initial questions

**Example Greeting:**
```
Hello! 👋 Welcome to TalentScout, an AI-powered hiring assistant.

I'm here to get to know you better and understand your professional 
background. Let's start with some basic information:

1. What's your full name?
2. What's your contact (email or phone)?
3. How many years of experience do you have?
4. What positions are you interested in?

Feel free to share as much detail as you'd like!
```

### Step 2: Share Your Information

Type naturally in the chat input box at the bottom:
```
"Hi! I'm Sarah Chen, you can reach me at sarah@example.com. 
I have 5 years of experience in full-stack development."
```

**What TalentScout Extracts:**
- ✅ Name: "Sarah Chen"
- ✅ Contact: "sarah@example.com"
- ✅ Experience: 5 years

### Step 3: Discuss Your Tech Stack

Continue the conversation naturally:
```
"I mostly work with Python and JavaScript. I use React for frontend 
and Django for backend. I'm very comfortable with PostgreSQL and Docker."
```

**Automatic Detection:**
- Languages: `python`, `javascript`
- Frameworks: `react`, `django`
- Tools: `docker`, `postgresql`
- No need to separate or format - TalentScout detects automatically

### Step 4: Answer Follow-Up Questions

TalentScout may ask:
```
"That's a great foundation! Since you work with React, 
can you tell me your approach to state management? Do you prefer 
Context API, Redux, or something else?"
```

**Tips for Good Responses:**
- Be specific with examples
- Explain your reasoning
- Share real project experiences
- Mention both strengths and learning areas

### Step 5: Monitor Sidebar Summary

As you chat, the sidebar updates in real-time:
```
📊 Candidate Summary
┌─────────────────────┐
│ Experience: 5 yrs   │
│ Tech Stack: 7       │
├─────────────────────┤
Positions:
- full stack

Technologies:
python, javascript, react, django, ...
```

---

## Advanced Features

### Generating Technical Questions

After sharing your tech stack:

1. Click **🎯 Generate Technical Questions** button
2. Wait for AI to create tailored questions
3. Questions will appear in the chat

**Question Generation Process:**
- Analyzes your experience level (Junior/Mid/Senior/Expert)
- Considers your job interests
- Creates 3-5 relevant questions
- Covers: conceptual, practical, architectural skills

**Example Generated Questions:**
```
Technical Questions Generated:

1. **React State Management Challenge**
   - Question: How would you structure state for a complex dashboard?
   - Assessment: Advanced React patterns and scalability
   - Expected: Discussion of Context, Redux, or custom hooks

2. **Database Design**
   - Question: Design a database schema for an e-commerce platform
   - Assessment: SQL knowledge and normalization concepts
   - Expected: Proper relationships, indexing strategy

3. **API Security**
   - Question: How do you handle authentication in REST APIs?
   - Assessment: Security best practices
   - Expected: JWT tokens, CORS, encryption discussion
```

### Finalizing the Interview

When interview is complete:

1. Click **✅ Finalize Interview** button
2. Chatbot generates closing summary:

```
Thank you for this productive conversation! Here's your summary:

📋 Your Profile:
- Experience: 5 years
- Technical Stack: python, javascript, react, django, docker, postgresql
- Positions Interested: full-stack

📝 Next Steps:
We'll review your information and get back to you within 48 hours.
Check your email (sarah@example.com) for updates.

Looking forward to the next stage! 🚀
```

### Exporting Interview Data

1. Click **📥 Export Interview Data** button
2. System generates unique Candidate ID

**Output:**
```
✅ Interview data exported with ID: cand_20260410_143022

📝 Candidate ID: cand_20260410_143022
```

**Where Data is Stored:**
- File: `data/candidates.json`
- Conversation: `data/conversations.json`

**Exported Data Includes:**
- Candidate name, contact, experience
- Detected tech stack
- Job interests
- Full conversation history
- Interview timestamp

### Viewing Saved Data

To review candidate information:

1. Open `data/candidates.json` in text editor
2. Find by Candidate ID
3. View complete profile

**Example Data Structure:**
```json
{
  "cand_20260410_143022": {
    "id": "cand_20260410_143022",
    "name": "Sarah Chen",
    "contact": "sarah@example.com",
    "experience_years": 5,
    "positions_interested": ["full-stack"],
    "tech_stack": ["python", "react", "django", "postgresql", "docker"],
    "created_at": "2026-04-10T14:30:22"
  }
}
```

---

## Tips & Best Practices

### For Better Interview Results

✅ **DO:**
- Share specific project examples
- Mention frameworks and versions
- Discuss your learning journey
- Ask clarifying questions
- Be honest about strengths and weaknesses

❌ **DON'T:**
- Give one-word answers
- Claim technologies you haven't used
- Interrupt the conversation flow
- Share confidential company information
- Exaggerate experience levels

### Tech Stack Sharing Tips

**Good Example:**
```
"I've been using Python for 5 years, primarily with Django for backend. 
I've also worked with FastAPI for microservices. On the frontend, I'm 
comfortable with React using TypeScript, and I've recently started 
exploring Vue.js. For databases, I use PostgreSQL and have some 
experience with MongoDB."
```

**Information Extracted:**
- Languages: python
- Frameworks: django, fastapi, react, vue
- Tools: typescript, postgresql, mongodb
- Experience depth: Clear progression

### Managing Multiple Interviews

**Conduct Several Interviews:**
1. Complete first interview → Click "Start New Interview"
2. Chatbot resets for new candidate
3. Previous data auto-saves
4. Begin new interview with fresh candidate

**Accessing Previous Interviews:**
1. Check `data/candidates.json`
2. Match Candidate ID to find information
3. Use ID for records/follow-up

---

## Troubleshooting

### Issue: API Key Error
```
⚠️ OpenAI API key not found. 
Please set OPENAI_API_KEY environment variable.
```

**Solution:**
1. Create `.env` file in project root
2. Add: `OPENAI_API_KEY=sk-your_key`
3. Save file
4. Refresh browser (Streamlit will auto-reload)

### Issue: Module Import Error
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
1. Verify virtual environment is activated
2. Run: `pip install -r requirements.txt`
3. Restart streamlit: `ctrl+c` then `streamlit run streamlit_app.py`

### Issue: Slow Responses
```
⏳ Thinking... (takes > 10 seconds)
```

**Causes & Solutions:**
- OpenAI API is slow → Wait or check status
- Internet connection issue → Check connectivity
- High load → Try again in few minutes
- Token limit reached → Use shorter messages

### Issue: Data Not Saving
```
Interview completed but no data saved
```

**Solution:**
1. Check `data/` folder exists
2. Verify write permissions
3. Check file not corrupted: `python -m json.tool data/candidates.json`

### Issue: Chatbot Gives Irrelevant Answers

**Possible Cause:** 
- System prompt misconfigured
- API call failed silently

**Solution:**
1. Restart application: `ctrl+c` then rerun
2. Check internet connection
3. Verify OpenAI account has credits

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Stop Streamlit server |
| `R` | Refresh page in browser |
| `Tab` | Focus chat input |
| `Enter` | Send message |
| `Shift+Enter` | New line in message |

---

## Performance Tips

1. **Clear Browser Cache** if app behaves oddly
   - Ctrl+Shift+Delete → Clear Cache

2. **Use Modern Browser**
   - Chrome, Firefox, Edge recommended
   - Safari works but may have small UI issues

3. **Monitor System Resources**
   - Streamlit uses ~200MB RAM
   - OpenAI API uses network bandwidth
   - Close other heavy applications for better performance

---

## FAQ

**Q: Can I have multiple people interviewed simultaneously?**
A: Yes! Open multiple browser windows/tabs. Each maintains separate state.

**Q: How long does an interview take?**
A: Typically 10-15 minutes for complete interview including questions.

**Q: Can I edit candidate information after saving?**
A: Not through UI. Manually edit `data/candidates.json` file.

**Q: Is my data secure?**
A: Data stored locally. For production, implement encryption and secure storage.

**Q: Can I use GPT-3.5 instead of GPT-4?**
A: Yes! Edit `src/config.py`:
   ```python
   MODEL_NAME = "gpt-3.5-turbo"  # Faster, cheaper
   ```

**Q: How do I reset all data?**
A: Delete `data/candidates.json` and `data/conversations.json` files.

---

## Support Resources

- **Readme**: See [README.md](README.md) for overview
- **Tech Details**: See [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) for architecture
- **OpenAI Docs**: https://platform.openai.com/docs/api-reference/chat/create
- **Streamlit Docs**: https://docs.streamlit.io/

---

**Version**: 1.0  
**Last Updated**: April 10, 2026
