from abc import ABC, abstractmethod

class BaseGrader(ABC):
    @abstractmethod
    def grade(self, problem_data, student_code):
        pass

    def format_user_prompt(self, problem_data, student_code):
        """Prepares all the data from benchmark.json for the LLM."""
        
        # We extract test cases and format them as a readable string
        test_cases_str = ""
        for i, tc in enumerate(problem_data.get('test_cases', [])):
            test_cases_str += f"- Test {i+1}: Input '{tc['input']}' -> Expected Output '{tc['expected_output']}' ({tc['description']})\n"

        return f"""
        --- PROBLEM DATA ---
        TITLE: {problem_data['title']}
        DESCRIPTION: {problem_data['problem_description']}
        EXPLICIT INSTRUCTIONS: {problem_data.get('explicit_instructions', 'N/A')}

        --- FUNCTIONAL TEST CASES ---
        Use these to verify if the student code actually works:
        {test_cases_str}

        --- TEACHER'S REFERENCE SOLUTION ---
        Use this as a logical guide, not for character-by-character matching:
        {problem_data['reference_solution']}

        --- GRADING RUBRIC ---
        LOGIC POINTS: {problem_data['grading_rubric']['logic_points']}
        SYNTAX POINTS: {problem_data['grading_rubric']['syntax_points']}
        
        HIDDEN DEDUCTIONS (Apply these based on exclusivity groups):
        {problem_data['grading_rubric']['hidden_deductions']}

        --- STUDENT SUBMISSION TO GRADE ---
        CODE:
        {student_code}

        --- FINAL TASK ---
        1. Mentally execute the student code with the TEST CASES provided.
        2. Compare logic with the REFERENCE SOLUTION.
        3. Subtract points using the RUBRIC and HIDDEN DEDUCTIONS.
        4. Respond ONLY in the requested JSON format.
        """