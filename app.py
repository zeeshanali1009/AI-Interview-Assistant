import streamlit as st
from modules.jobdesc_loader import load_jobdesc
from modules.resume_loader import load_resume
from modules.vector_store import build_vector_store, query_vector_store
from modules.interview_engine import generate_interview_questions
from modules.chat_engine import get_answer

st.set_page_config(page_title="🤖 AI Interview Assistant", layout="wide")

st.title("🎯 AI Interview Assistant")
st.write("Upload your **Resume** and **Job Description**, then chat with the AI interviewer!")

# File uploads
resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx", "txt"])
jobdesc_file = st.file_uploader("🧾 Upload Job Description", type=["pdf", "docx", "txt"])

if resume_file and jobdesc_file:
    resume_text = load_resume(resume_file)
    jd_text = load_jobdesc(jobdesc_file)

    st.success("✅ Files uploaded successfully!")

    # Build FAISS index
    st.info("🔍 Building vector store for contextual matching...")
    index, embeddings, texts = build_vector_store([resume_text, jd_text])
    st.success("📚 Data indexed successfully!")

    # Generate AI interview questions
    if st.button("🎤 Generate Interview Questions"):
        st.info("🤖 Generating questions based on your resume & job description...")
        questions = generate_interview_questions(resume_text, jd_text)
        st.session_state.questions = questions
        st.success("✅ Interview questions ready!")

    # Display and answer
    if "questions" in st.session_state:
        st.subheader("💬 Interview Simulation")
        question = st.selectbox("Select a question:", st.session_state.questions)

        if st.button("Get AI’s Suggested Answer"):
            context = query_vector_store(question, index, embeddings, texts)
            answer = get_answer(question, context)
            st.text_area("🧠 Suggested Answer:", value=answer, height=200)
else:
    st.warning("Please upload both files to start.")
