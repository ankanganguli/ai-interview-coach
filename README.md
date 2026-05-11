
# AI Mock Interview Coach (POC)
This is a multi-agent system designed to conduct realistic, adaptive mock interviews for professional roles. Unlike static chatbots, this system uses a **Sequential Agent Orchestration** pattern to probe candidate depth and provide a high-level feedback report at the end of the session.
## 🌐 Live Demo
You can test the application immediately at the following link:
Https://ai-interview-coach-usnpyzrzhzeq7dyif8jchv.streamlit.app/
## 🏗 Architecture Overview
The system is built on an agentic workflow where three distinct personas collaborate to manage the session:
 1. **The Evaluator (Logic Agent)**: Works silently in the background to analyze the user's response for technical depth, clarity, and "messiness" like vague answers or "I don't know".
 2. **The Interviewer (Adaptive Agent)**: Manages the conversation. It consumes the Evaluator's findings to decide whether to probe deeper into a weak answer or move on to a new topic.
 3. **The Coach (Feedback Agent)**: Activates after the final turn to analyze the full transcript and generate a structured performance report covering strengths, gaps, and specific things to practice.
## 🚀 How to Run Locally
If you prefer to run the prototype in a local environment:
 1. **Install Dependencies**: Run pip install -r requirements.txt.
 2. **Launch the Application**: Execute the following command in your terminal:
   ```bash
   streamlit run app.py
   
   ```
## 🧠 Key Design Decisions
 * **Sequential Orchestration**: I implemented a sequential flow (Evaluator → Interviewer) to ensure every question is grounded in an objective analysis of the candidate's last answer, fulfilling the "Intelligent Follow-up" requirement.
 * **Model Selection**: I utilized **Gemini 3.1 flash - lite** for this POC to balance high-level intelligence with the low latency required for a real-time conversational interface.
 * **Modular Prompting**: All agent personas are isolated in the prompts/ directory. This allows for easy updates to the interview logic without modifying the core Python code.
## 📝 Example Interview Transcripts
Here are three scenarios demonstrating how the system adapts to different candidate inputs:
### 1. Strong Candidate (Technical Depth)
 * **Interviewer**: "...elaborate on your experience with PyTorch... such as DistributedDataParallel, custom Autograd functions, or torchvision."
 * **Candidate**: "I have used torchvision."
 * **Adaptive Response**: "Since we have established that you have utilized torchvision, I need to see how you apply these tools in a production or research workflow. Could you specify which components you relied on—such as pre-trained model architectures or transforms?"
### 2. Weak Candidate (Probing Logic)
 * **Interviewer**: "...provide more context regarding your technical background and your professional goals?"
 * **Candidate**: "No"
 * **Adaptive Response**: "Ankan, your response is insufficient for a professional interview. As this role requires high-level technical proficiency and clear communication, I need to understand your qualifications to proceed."
### 3. Edge Case (Handling "I don't know")
 * **Interviewer**: "...what tools did you use to process that data, and how did you verify that your results were accurate?"
 * **Candidate**: "I don't know"
 * **Adaptive Response**: "Thank you for being honest. Let's look at a foundational piece instead. If I gave you a small spreadsheet, what is the first thing you would check to ensure the data is clean?"
### 📂 Project Structure
 * **app.py**: Main UI and orchestration logic.
 * **prompts/**: Directory containing interviewer.txt, evaluator.txt, and coach.txt.
 * **requirements.txt**: List of necessary Python packages.
 * **.gitignore**: Security configuration to protect local secrets.
