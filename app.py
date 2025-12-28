import streamlit as st
import json
from agent.few_cot_grader import FewShotCoTGrader

# --- PAGE CONFIG ---
st.set_page_config(page_title="LLM C++ Grading Agent", page_icon="🎓", layout="wide")

# --- INITIALIZE AGENT ---
# We use st.cache_resource so the agent doesn't reload every time you click a button
@st.cache_resource
def get_grader():
    return FewShotCoTGrader()

grader = get_grader()

# --- UI HEADER ---
st.title("🎓 LLM-Based C++ Grading Agent")
st.markdown("Automated grading using **Few-Shot Chain-of-Thought** reasoning.")
st.divider()

# --- LAYOUT: TWO COLUMNS ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📋 Teacher Configuration")
    
    problem_title = st.text_input("Problem Title", placeholder="e.g., Factorial Logic")
    
    problem_desc = st.text_area("Problem Description", height=150, 
                                placeholder="Describe what the student needs to do...")
    
    reference_sol = st.text_area("Teacher Reference Solution (C++)", height=200, 
                                 placeholder="Paste the perfect code here...")
    
    # We provide a default JSON structure for the rubric to help the teacher
    default_rubric = {
        "logic_points": 16,
        "syntax_points": 4,
        "hidden_deductions": [
            {"condition": "Description of error", "deduct": 5, "exclusivity_group": "group1"}
        ]
    }
    rubric_json = st.text_area("Grading Rubric (JSON Format)", 
                               value=json.dumps(default_rubric, indent=2), height=200)

with col2:
    st.header("💻 Student Submission")
    
    student_name = st.text_input("Student Name", placeholder="e.g., John Doe")
    
    student_code = st.text_area("Student C++ Code", height=450, 
                                 placeholder="Paste student code here...")
    
    grade_button = st.button("🚀 Grade Submission", use_container_width=True)

# --- GRADING LOGIC ---
if grade_button:
    if not problem_desc or not student_code or not reference_sol:
        st.error("Please fill in the Problem Description, Reference Solution, and Student Code.")
    else:
        with st.spinner("Agent is analyzing code... Please wait."):
            try:
                # 1. Prepare data for the agent
                problem_data = {
                    "title": problem_title,
                    "problem_description": problem_desc,
                    "reference_solution": reference_sol,
                    "grading_rubric": json.loads(rubric_json)
                }
                
                # 2. Call the Agent
                result = grader.grade(problem_data, student_code)
                
                # 3. Display Results
                st.divider()
                st.header(f"📊 Results for {student_name}")
                
                res_col1, res_col2, res_col3 = st.columns(3)
                res_col1.metric("Final Score", f"{result.get('final_score', 0)} / 20")
                res_col2.metric("Logic", f"{result.get('score_breakdown', {}).get('logic', 0)}")
                res_col3.metric("Syntax", f"{result.get('score_breakdown', {}).get('syntax', 0)}")
                
                st.subheader("📝 AI Feedback")
                st.info(result.get("feedback", "No feedback provided."))
                
                with st.expander("See Detailed Chain-of-Thought Analysis"):
                    st.write(result.get("analysis", "No analysis available."))
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write(" **Strategy:** Few-Shot CoT")
st.sidebar.write(" **LLM:** Llama-3.3-70b (via Groq)")