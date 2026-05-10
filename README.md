This is the finalized, professional README.md for your submission. It is structured specifically to tick every box mentioned in your assignment document, including the multi-agent architecture, design tradeoffs, and the specific transcripts you just generated.
# AI Mock Interview Coach (POC)
This is a multi-agent system designed to conduct realistic, adaptive mock interviews for professional roles. Unlike static chatbots, this system uses a **Sequential Agent Orchestration** pattern to probe candidate depth and provide structured feedback.
## 🏗 Architecture Overview
The system is built on an agentic workflow where three distinct personas collaborate to manage the session:
 1. **The Evaluator (Logic Agent):** Works silently in the background. It analyzes the user's response for technical depth, clarity, and "messiness" like vague answers or "I don't know".
 2. **The Interviewer (Adaptive Agent):** Manages the conversation. It consumes the Evaluator's findings (eval_data) to decide whether to probe deeper into a weak answer or move on to a new topic.
 3. **The Coach (Feedback Agent):** Activates after the final turn to analyze the full transcript and generate a structured performance report covering strengths, gaps, and practice areas.
## 🚀 Setup & Run
 
 1. **Install Dependencies:** pip install -r requirements.txt
 2. **Configure API Key:** Create a .streamlit/secrets.toml file and add your key:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   
   ```
   *(Note: For the reviewer's convenience, the shared ZIP version includes a pre-configured key for immediate testing)*.
 4. **Launch the App:** streamlit run app.py
## 🧠 Key Design Decisions & Tradeoffs
 * **Sequential Orchestration:** I implemented a sequential flow (Evaluator → Interviewer) to ensure every question is grounded in an objective analysis of the candidate's last answer, fulfilling the "Intelligent Follow-up" requirement.
 * **Model Selection:** I utilized **Gemini 3.1 Flash-Lite** (May 2026 Stable Release). I chose this over heavier models to prioritize ultra-low latency, ensuring the conversation feels natural rather than having long "thinking" delays.
 * **Modular Prompting:** All agent personas are isolated in the prompts/ directory. This allows for quick updates to the interview "personality" without touching the core orchestration logic.
 * **Stateful Memory:** Streamlit session_state is used to track the 5–7 turn limit and maintain a clean transcript for the final Coaching phase.
## 📝 Example Interview Transcripts
As required by the assignment, here are three scenarios demonstrating system behavior:
### 1. Strong Candidate (Technical Depth)
 * **Interviewer:** "...elaborate on your experience with PyTorch... such as DistributedDataParallel, custom Autograd functions, or torchvision."
 * **Candidate:** "I have used torchvision."
 * **System Logic:** Evaluator flagged the mention of a specific library but noted a lack of implementation detail.
 * **Adaptive Response:** "Since we have established that you have utilized torchvision, I need to see how you apply these tools... Could you specify which components you relied on—such as pre-trained model architectures or transforms?"
### 2. Weak Candidate (Probing Logic)
 * **Interviewer:** "...provide more context regarding your technical background... and your professional goals?"
 * **Candidate:** "No"
 * **System Logic:** The Evaluator flagged "Professionalism Gap" and "Insufficient Input".
 * **Adaptive Response:** "Ankan, your response is insufficient for a professional interview... If you are unwilling or unable to elaborate on your experience, I cannot move forward with your candidacy."
### 3. Edge Case (Handling "I don't know")
 * **Interviewer:** "...what tools did you use to process that data, and how did you verify that your results were accurate?"
 * **Candidate:** "I don't know"
 * **System Logic:** The system recognized a gap in end-to-end experience and pivoted to a foundational question to find the candidate's current knowledge ceiling.
 * **Adaptive Response:** "Thank you for being honest. Let's look at a foundational piece instead. If I gave you a small spreadsheet, what is the *first* thing you would check to ensure the data is clean?"
### 📂 Project Structure
 * app.py: Main UI and orchestration logic.
 * prompts/: Directory containing interviewer.txt, evaluator.txt, and coach.txt.
 * requirements.txt: List of necessary Python packages.
