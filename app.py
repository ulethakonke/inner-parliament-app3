import streamlit as st
import openai
import os

# --- CONFIGURE OPENAI ---
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# --- Soulfile Prompt Templates ---
soulfiles = {
    "The Trickster": {
        "style": "confident, playful, misleading",
        "description": "Sometimes lies. Often mocks. Always confident.",
        "system": "You are The Trickster, a confident, playful, and occasionally misleading persona. You speak in riddles, dodge questions, and give answers that make people think twice."
    },
    "The Healer": {
        "style": "gentle, reflective, nurturing",
        "description": "Affirms your feelings, avoids harsh logic.",
        "system": "You are The Healer, a gentle and reflective voice that soothes and nurtures. You respond with emotional intelligence and spiritual calm."
    },
    "The Analyst": {
        "style": "logical, precise, skeptical",
        "description": "Dissects assumptions, minimizes emotion.",
        "system": "You are The Analyst, a hyper-logical and skeptical voice. You analyze questions methodically and avoid emotional interpretation."
    }
}

# --- OpenAI Response Function ---
def ask_openai(system_prompt, user_question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# --- UI Setup ---
st.set_page_config(page_title="Inner Parliament", layout="centered")
st.title("🧠 Inner Parliament")
st.markdown("_Ask a question. Get answers from different minds inside you._")

# --- User Input ---
user_question = st.text_input("What’s on your mind?", placeholder="e.g. Should I start over?", key="user_q")

# --- Response Section ---
if user_question:
    st.divider()
    for name, soul in soulfiles.items():
        with st.container():
            st.subheader(name)
            st.caption(soul['description'])
            st.markdown(f"**Style:** _{soul['style']}_")
            response = ask_openai(soul['system'], user_question)
            st.write(f"> {response}")
    st.divider()
    st.markdown("✳️ _These voices are fictional personas. You choose what resonates._")
