import asyncio
import streamlit as st
from models.schemas import UserRequest
from agents.orchestrator import orchestrate_instruction_generation

st.set_page_config(
    page_title="Code Instructor",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Code Instruction Generator")
st.markdown(
    """
    This tool generates step-by-step coding instructions from natural language descriptions.
    It uses AI to create detailed instructions, find relevant documentation, and suggest
    debugging tips.
    """
)

with st.sidebar:
    st.header("About")
    st.info(
        """
        Powered by:
        - Gemini 2.0 Flash AI
        - PydanticAI
        - Streamlit
        
        This multi-agent system helps you understand how to implement coding tasks
        with detailed instructions.
        """
    )
    
    st.header("Features")
    st.markdown(
        """
        - Step-by-step coding instructions
        - Relevant documentation references
        - Debugging tips and common pitfalls
        - Support for multiple programming languages
        """
    )

st.header("What would you like to build?")

with st.form("task_form"):
    task_description = st.text_area(
        "Describe your coding task",
        placeholder="E.g., Create a Python function that connects to a database and retrieves user data"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox(
            "Programming Language",
            options=["Python", "JavaScript", "Java", "C++", "Go", "Ruby", "Rust", "PHP", "Swift", "TypeScript"],
            index=0
        )
    with col2:
        complexity = st.selectbox(
            "Complexity Level",
            options=["beginner", "intermediate", "advanced"],
            index=1
        )
    
    submit_button = st.form_submit_button("Generate Instructions")

if submit_button and task_description:
    request = UserRequest(
        task_description=task_description,
        language=language,
        complexity=complexity
    )
    
    with st.spinner("Generating your coding instructions..."):
        try:
            result = asyncio.run(orchestrate_instruction_generation(request))
            
            st.success("Instructions generated successfully!")
            
            with st.expander("Step-by-Step Instructions", expanded=True):
                st.markdown(f"## {result.instructions.description}")
                for i, (step, code) in enumerate(zip(result.instructions.steps, result.instructions.code_snippets), 1):
                    st.markdown(f"### Step {i}: {step}")
                    st.code(code, language=language.lower())
            
            with st.expander("Documentation References", expanded=True):
                if result.references:
                    for ref in result.references:
                        st.markdown(f"### {ref.title}")
                        if ref.url:
                            st.markdown(f"[View Documentation]({ref.url})")
                        st.markdown(ref.content)
                        st.markdown("---")
                else:
                    st.info("No specific references found for this task.")
            
            with st.expander("Debugging Tips", expanded=True):
                if result.debug_suggestions:
                    for i, debug in enumerate(result.debug_suggestions, 1):
                        st.markdown(f"### Issue {i}: {debug.issue}")
                        st.markdown(f"**Solution:** {debug.solution}")
                        st.markdown(f"**Explanation:** {debug.explanation}")
                        st.markdown("---")
                else:
                    st.info("No specific debugging suggestions for this task.")
            
            st.markdown("## Summary")
            st.markdown(result.summary)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.markdown("Please try again or modify your request.")
else:
    if submit_button:
        st.warning("Please provide a description of your coding task.")
