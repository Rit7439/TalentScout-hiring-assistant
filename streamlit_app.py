"""Main Streamlit application for TalentScout hiring assistant."""

import os
from dotenv import load_dotenv

# Load environment variables FIRST — before any src imports that call os.getenv()
load_dotenv()

import streamlit as st
from src.chatbot import TalentScoutChatbot
from src.config import APP_TITLE, APP_DESCRIPTION, DATA_PRIVACY_NOTICE

# Configure Streamlit
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state."""
    if "api_key_valid" not in st.session_state:
        from src.config import GROQ_API_KEY
        st.session_state.api_key_valid = bool(GROQ_API_KEY)

    if "chatbot" not in st.session_state:
        if st.session_state.api_key_valid:
            try:
                st.session_state.chatbot = TalentScoutChatbot()
                st.session_state.interview_started = False
                st.session_state.messages = []
            except ValueError as e:
                st.session_state.chatbot = None
                st.session_state.interview_started = False
                st.session_state.messages = []
        else:
            st.session_state.chatbot = None
            st.session_state.interview_started = False
            st.session_state.messages = []


def display_header():
    """Display application header."""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🤖 " + APP_TITLE)
        st.markdown(f"*{APP_DESCRIPTION}*")
    with col2:
        st.info("👤 Interview Assistant v1.0")


def display_sidebar():
    """Display sidebar with options."""
    with st.sidebar:
        st.header("📋 Interview Controls")
        
        if st.button("🚀 Start New Interview", use_container_width=True):
            st.session_state.chatbot = TalentScoutChatbot()
            st.session_state.messages = []
            st.session_state.interview_started = True
            st.rerun()
        
        st.divider()
        
        # Display candidate summary
        if st.session_state.messages:
            st.subheader("📊 Candidate Summary")
            summary = st.session_state.chatbot.get_candidate_summary()
            
            col1, col2 = st.columns(2)
            with col1:
                if summary.get("experience_years"):
                    st.metric("Experience", f"{summary['experience_years']} yrs")
            with col2:
                if summary.get("tech_stack"):
                    st.metric("Tech Stack", len(summary["tech_stack"]))
            
            if summary.get("positions_interested"):
                st.write("**Positions:** " + ", ".join(summary["positions_interested"]))
            
            if summary.get("tech_stack"):
                st.write("**Technologies:** " + ", ".join(summary["tech_stack"]))
        
        st.divider()
        
        # Display data privacy notice
        st.warning(DATA_PRIVACY_NOTICE)


def display_chat_interface():
    """Display chat interface."""
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Your response..."):
        # Add user message to display
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.process_message(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


def display_controls():
    """Display interview control buttons."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.messages and st.button("🎯 Generate Technical Questions"):
            with st.spinner("Generating questions..."):
                questions = st.session_state.chatbot.generate_technical_questions()
                st.info(questions)
    
    with col2:
        if st.session_state.messages and st.button("✅ Finalize Interview"):
            with st.spinner("Finalizing..."):
                closing = st.session_state.chatbot.finalize_interview()
                with st.chat_message("assistant"):
                    st.markdown(closing)
                st.session_state.messages.append({"role": "assistant", "content": closing})
                st.success("Interview completed! Candidate data saved.")
                candidate_id = st.session_state.chatbot.export_interview_data()
                if candidate_id:
                    st.info(f"📝 Candidate ID: `{candidate_id}`")
    
    with col3:
        if st.button("📥 Export Interview Data"):
            if not st.session_state.messages:
                st.warning("Start an interview first to export data.")
            else:
                candidate_id = st.session_state.chatbot.export_interview_data()
                if candidate_id:
                    st.success(f"✅ Data saved! Candidate ID: `{candidate_id}`")
                    summary = st.session_state.chatbot.get_candidate_summary()
                    st.json({
                        "candidate_id": candidate_id,
                        "name": summary.get("name", "N/A"),
                        "contact": summary.get("contact", "N/A"),
                        "experience_years": summary.get("experience_years", "N/A"),
                        "tech_stack": summary.get("tech_stack", []),
                        "positions_interested": summary.get("positions_interested", []),
                    })
                    st.caption("📁 Saved to: `data/candidates.json` and `data/conversations.json`")
                else:
                    st.warning("No candidate information collected yet. Please share your details in the chat first.")


def main():
    """Main application function."""
    initialize_session_state()
    display_header()

    # Check Groq API key
    if not st.session_state.api_key_valid:
        st.error("⚠️ Groq API Key Not Configured")
        st.markdown("""
### Setup Required

TalentScout needs a **free** Groq API key to function. Follow these steps:

**Step 1: Get Your Free API Key**
- Visit [Groq Console](https://console.groq.com/keys)
- Sign up (it's free!) and click **"Create API Key"**
- Copy the key

**Step 2: Add It to the `.env` File**
In the project root (`TalentScout HIRING/`), open or create the `.env` file and add:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

**Step 3: Restart the App**
```bash
streamlit run streamlit_app.py
```

> ✅ Groq is **completely free** with generous limits — no credit card needed!
        """)
        return

    st.success(f"⚡ Powered by Groq — `llama-3.1-8b-instant` (ultra-fast, free cloud inference)")

    display_sidebar()
    
    st.divider()
    
    # Start interview if not started
    if not st.session_state.interview_started and not st.session_state.messages:
        if st.button("🎬 Begin Interview"):
            st.session_state.interview_started = True
            greeting = st.session_state.chatbot.start_interview()
            st.session_state.messages.append({"role": "assistant", "content": greeting})
            st.rerun()
    
    # Display chat interface
    if st.session_state.interview_started or st.session_state.messages:
        display_chat_interface()
        st.divider()
        display_controls()
    else:
        st.markdown("""
        ## 👋 Welcome to TalentScout!
        
        Click **Begin Interview** to start an intelligent hiring conversation. The chatbot will:
        
        ✨ **Features:**
        - 📝 Collect essential candidate information
        - 🔍 Detect tech stack and skills
        - 💡 Generate relevant technical questions
        - 💾 Save structured interview data
        - 🔒 Maintain data privacy compliance
        
        **Get Started:**
        1. Click "Begin Interview" below
        2. Share your information naturally
        3. Answer technical questions
        4. View interview summary
        """)


if __name__ == "__main__":
    main()
