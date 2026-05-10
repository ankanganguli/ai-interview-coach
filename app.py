import streamlit as st
import google.generativeai as genai
import json
import time

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="AI Mock Interview Coach", layout="wide")

# Check for API Key in Streamlit Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing GEMINI_API_KEY in .streamlit/secrets.toml")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Using the newest stable May 2026 model for speed and zero cost
model = genai.GenerativeModel('gemini-3.1-flash-lite')

# --- 2. HELPER FUNCTIONS ---
def get_prompt(agent_name):
    """Loads agent personas from the prompts/ folder."""
    try:
        with open(f"prompts/{agent_name}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "You are a professional AI interview assistant."

# --- 3. SESSION STATE (Memory) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0
if "is_finished" not in st.session_state:
    st.session_state.is_finished = False

# --- 4. SIDEBAR SETUP ---
with st.sidebar:
    st.title("Interview Scope")
    role = st.text_input("Target Role", value="AI Engineer Intern")
    focus = st.selectbox("Focus Area", ["Technical", "Behavioral"])
    st.info(f"Turns Completed: {st.session_state.turn_count} / 7")
    
    if st.button("Reset Interview"):
        st.session_state.clear()
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.title("🤖 AI Mock Interview Coach")
st.markdown(f"**Role:** {role} | **Focus:** {focus}")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INITIAL GREETING (Now Dynamic) ---
if not st.session_state.chat_history:
    # This text now pulls directly from your sidebar variables
    welcome_text = (
        f"Hello! I'm your interviewer for the **{role}** position. "
        f"We'll focus on **{focus}** questions today. "
        "To get started, can you tell me a bit about your background?"
    )
    st.session_state.chat_history.append({"role": "assistant", "content": welcome_text})
    st.rerun()


# --- 6. AGENTIC INTERACTION LOGIC ---
if st.session_state.turn_count < 7 and not st.session_state.is_finished:
    if user_input := st.chat_input("Your response..."):
        # Save user response
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.turn_count += 1
        
        # Visible Multi-Agent Collaboration
        with st.status("🔍 Agentic Workflow Active...", expanded=True) as status:
            
            # Agent 1: Evaluator
            st.write("🤖 **Evaluator Agent:** Analyzing response for technical gaps...")
            e_prompt = get_prompt("evaluator")
            e_res = model.generate_content(f"{e_prompt}\n\nCandidate: {user_input}")
            evaluation = e_res.text # Fixes NameError
            
            # Agent 2: Interviewer
            st.write("🎤 **Interviewer Agent:** Adjusting persona and follow-up...")
            i_prompt = get_prompt("interviewer").format(
                role=role, 
                focus=focus, 
                turn=st.session_state.turn_count,
                eval_data=evaluation
            )
            
            # Generate Final Answer
            history_context = str(st.session_state.chat_history)
            ai_res = model.generate_content(f"System: {i_prompt}\n\nHistory: {history_context}")
            
            status.update(label="✅ Response Synthesized", state="complete", expanded=False)

        # Show AI Response
        with st.chat_message("assistant"):
            st.markdown(ai_res.text)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_res.text})
        
        st.rerun()

# --- 7. FINAL COACHING PHASE ---
elif st.session_state.turn_count >= 7 and not st.session_state.is_finished:
    st.session_state.is_finished = True
    st.balloons()
    
    with st.spinner("Generating your final performance report..."):
        # Agent 3: Coach
        c_prompt = get_prompt("coach")
        transcript = str(st.session_state.chat_history)
        feedback = model.generate_content(f"System: {c_prompt}\n\nTranscript: {transcript}")
        
        st.success("Analysis Complete!")
        st.header("🏁 Final Coaching Report")
        st.markdown(feedback.text)
