import streamlit as st
import json
import pandas as pd
from agent.few_cot_grader import FewShotCoTGrader

# --- PAGE CONFIG ---
st.set_page_config(page_title="LLM C++ Grading Agent", page_icon="🎓", layout="wide")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stDataFrame { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE AGENT ---
@st.cache_resource
def get_grader():
    return FewShotCoTGrader()

grader = get_grader()

# --- SESSION STATE FOR DEMO PRESETS ---
# This allows the "Load Example" buttons to work
if 'p_title' not in st.session_state:
    st.session_state.p_title = ""
if 'p_desc' not in st.session_state:
    st.session_state.p_desc = ""
if 'p_ref' not in st.session_state:
    st.session_state.p_ref = ""
if 'p_rubric_list' not in st.session_state:
    st.session_state.p_rubric_list = [
        {"id": "R1", "condition": "Incorrect initialization", "deduct": 8, "group": "A"},
        {"id": "R2", "condition": "Wrong data type", "deduct": 4, "group": "B"},
    ]

# --- SIDEBAR: SYSTEM INFO & PRESETS ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.write("---")
    
    st.subheader("🚀 Quick Load Examples")


    if st.button("Find Max"):
        st.session_state.p_title = "Find Maximum in Array"
        st.session_state.p_desc = "Find the largest number in an array of size N. Must handle negative numbers."
        st.session_state.p_ref = "int findMax(int arr[], int n) {\n    int m = arr[0];\n    for(int i=1; i<n; i++) if(arr[i]>m) m=arr[i];\n    return m;\n}"
        st.session_state.p_rubric_list = [
            {"id": "R1", "condition": "Initialization fails for negative arrays (e.g. max=0)", "deduct": 6, "group": "A"},
            {"id": "R2", "condition": "Critical Bound Error: Loop goes out of array memory (e.g. i <= n)", "deduct": 6, "group": "B"},
            {
      "id": "R3",
      "condition": "Incorrect comparison operator (e.g., < instead of >)",
      "deduct": 8,
      "group": "comparison"
    }
        ]
        st.rerun()

    if st.button("Linked List: Insert at End"):
        st.session_state.p_title = "Linked List: Insert at End"
        st.session_state.p_desc = "Write a function 'Node* insertEnd(Node* head, int value)' that adds a new node to the end of a singly linked list. Return the head. Ensure proper initialization."
        st.session_state.p_ref = """struct Node {
    int data;
    Node* next;
};

Node* insertEnd(Node* head, int val) {
    Node* newNode = new Node{val, nullptr};
    if (head == nullptr) return newNode;
    
    Node* temp = head;
    while (temp->next != nullptr) {
        temp = temp->next;
    }
    temp->next = newNode;
    return head;
}"""
        st.session_state.p_rubric_list = [
            {"id": "R1", "condition": "Requirement: Handle empty list (head == NULL) correctly", "deduct": 4, "group": "safety"},
            {"id": "R2", "condition": "Requirement: Initialize 'next' pointer to NULL (prevent garbage)", "deduct": 4, "group": "memory"},
            {"id": "R3", "condition": "Requirement: Correct traversal to final node", "deduct": 6, "group": "logic"},
            {"id": "R4", "condition": "Requirement: Does not return the correct head", "deduct": 5, "group": "signature"}
        ]
        st.rerun()

    st.write("---")
    st.info(f"**Strategy:** Few-Shot CoT\n\n**LLM:** Llama-3.3-70B\n")

# --- UI HEADER ---
st.title("🎓 LLM-Based C++ Grading Agent")
st.markdown("Precision Grading using **Chain-of-Thought** reasoning.")
st.divider()

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Teacher Configuration")
    title_input = st.text_input("Problem Title", value=st.session_state.p_title)
    desc_input = st.text_area("Problem Description", value=st.session_state.p_desc, height=100)
    ref_input = st.text_area("Teacher Reference Solution (C++)", value=st.session_state.p_ref, height=200)
    
    st.write("**Grading Rubric (Editable Table)**")
    # Using data_editor instead of raw JSON box
    edited_df = st.data_editor(
        pd.DataFrame(st.session_state.p_rubric_list),
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small", help="Unique Rule ID (e.g. R1)"),
            "condition": st.column_config.TextColumn("Requirement Condition"),
            "deduct": st.column_config.NumberColumn("Deduct Points", min_value=0, max_value=16),
            "group": st.column_config.TextColumn("Group", width="small", help="Deductions in same group are not cumulative")
        }
    )

with col2:
    st.subheader("💻 Student Submission")
    s_name = st.text_input("Student Name", placeholder="Enter student's full name...")
    s_code = st.text_area("Paste Student C++ Code Here", height=435, placeholder="// Paste code here...")
    
    grade_button = st.button(" Run Grading Agent", use_container_width=True, type="primary")

# --- GRADING LOGIC ---
if grade_button:
    if not desc_input or not s_code or not ref_input:
        st.error("Please ensure all Problem and Student fields are filled!")
    else:
        with st.spinner("🤖 Agent is analyzing code logic..."):
            try:
                # Prepare data (Convert Table back to Agent's expected JSON structure)
                problem_data = {
                    "title": title_input,
                    "problem_description": desc_input,
                    "reference_solution": ref_input,
                    "grading_rubric": {
                        "logic_points": 16,
                        "syntax_points": 4,
                        "hidden_deductions": edited_df.to_dict('records')
                    }
                }
                
                # Execute Grader
                result = grader.grade(problem_data, s_code)
                
                # --- RESULTS DISPLAY ---
                st.balloons()
                st.divider()
                st.header(f"📊 Grading Report: {s_name}")
                
                # Metrics
                m1, m2, m3 = st.columns(3)
                f_score = result.get('final_score', 0)
                m1.metric("Final Score", f"{f_score} / 20")
                m2.metric("Logic Points", f"{result.get('score_breakdown', {}).get('logic', 0)} / 16")
                m3.metric("Syntax Points", f"{result.get('score_breakdown', {}).get('syntax', 0)} / 4")

                # Visual Feedback
                st.subheader("📝 AI Feedback")
                if f_score >= 15:
                    st.success(result.get("feedback"))
                elif f_score >= 10:
                    st.warning(result.get("feedback"))
                else:
                    st.error(result.get("feedback"))

                # Detailed Reasoning (The Doctor's Favorite Part)
                with st.expander("🔍 View Detailed Reasoning"):
                    st.write("The agent performed the following logical audit:")
                    st.info(result.get("analysis", "No analysis available."))

            except Exception as e:
                st.error(f"Error during grading: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 C++ Grading Agent Project")