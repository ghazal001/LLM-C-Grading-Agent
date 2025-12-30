This project is an ongoing LLM-based automated grading system designed to evaluate C++ programming assignments in a structured and objective manner. The system takes as input a problem description, a teacher reference solution, a grading rubric, and a student’s C++ code submission.

Using large language models and agent-based reasoning, the grading agent analyzes the student’s code, compares it with the reference solution, applies the rubric criteria, and generates a final numerical grade along with a detailed score breakdown and explanation. The output is produced in a structured JSON format to ensure consistency and easy integration with other systems.

The project explores different prompting and agentic strategies, including Chain-of-Thought reasoning, few-shot prompting, and evaluator-based workflows, and evaluates their effectiveness using a custom benchmark dataset with human-graded examples. A simple web interface is also included to demonstrate real-world usage of the grading system.

This project focuses on LLM reasoning, prompt engineering, AI agents, and practical AI system design for educational automation.

📘 How to Use This Grading System

1️⃣ Prerequisites

Make sure you have the following installed:

    Python 3.9+
    
    Git
    
    An LLM API key (Groq / OpenAI-compatible)

2️⃣ Clone the Repository

    git clone https://github.com/your-username/llm-cpp-grading-agent.git
    cd llm-cpp-grading-agent

3️⃣ Create a Virtual Environment (Recommended)

    python -m venv nlp_env
    source nlp_env/bin/activate  # Linux / macOS
    nlp_env\Scripts\activate     # Windows

4️⃣ Install Dependencies

    pip install -r requirements.txt

    Example requirements.txt
    streamlit
    openai>=1.0.0
    python-dotenv
    pydantic

5️⃣ Environment Configuration

    Create a .env file (DO NOT commit this file)
    cp .env.example .env
    

Edit .env and add your API key:

    GROQ_API_KEY=your_api_key_here
    LLM_MODEL=llama-3.3-70b-versatile


⚠️ .env is ignored by Git for security reasons.

6️⃣ Project Structure Overview

    grading_system_project/
    │
    ├── agent/                  # Grading agents (CoT, Few-shot, Evaluator, Voting)
    │   ├── base.py
    │   ├── cot_grader.py
    │   ├── few_cot_grader.py
    │   ├── evaluator_opt.py
    │   ├── voting_grader.py
    │
    ├── prompts/                # Prompt templates
    │   ├── cot_templates.py
    │   ├── few_shot_cot_templates.py
    │   ├── voting_templates.py
    │
    ├── benchmark/              # Human-labeled benchmark dataset
    │   └── benchmark.json
    │
    ├── experiments/            # Evaluation & comparison scripts
    │   ├── cot_vs_evaluator.py
    │   ├── voting_vs_cot_vs_few_cot_vs_evaluator_vs_human.py
    │
    ├── utils/                  # Utilities (LLM client, loaders, caching)
    │
    ├── app.py                  # Streamlit web interface
    ├── requirements.txt
    ├── .env.example
    └── README.md

7️⃣ Running the Grading Experiments

Compare different agentic strategies against human grades:

    python experiments/voting_vs_cot_vs_few_cot_vs_evaluator_vs_human.py


This script:

    Runs Zero-shot CoT
    
    Runs Few-shot CoT
    
    Runs Evaluator–Optimizer
    
    Runs Voting (Mean / Median)
    
    Compares all results against human scores
    
    Reports Mean Absolute Error (MAE)

8️⃣ Running the Web Interface (Demo)
    streamlit run app.py
    
    
    The web app allows you to:
    
    Select a problem from the benchmark
    
    Paste student C++ code
    
    Choose a grading strategy
    
    View structured grading output in real time

9️⃣ Output Format

All graders produce structured JSON output:

    {
      "analysis": "Explanation of reasoning",
      "score_breakdown": {
        "logic": 11,
        "syntax": 4
      },
      "final_score": 15,
      "feedback": "Clear feedback for the student"
    }
    

This makes the system easy to integrate into:

    LMS platforms
    
    Auto-grading pipelines
    
    Educational dashboards
