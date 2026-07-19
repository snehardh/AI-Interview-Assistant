import streamlit as st
import os
from dotenv import load_dotenv
from interview import generate_questions, evaluate_answer

load_dotenv()

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Interview Assistant")

# -------------------------------
# Session State
# -------------------------------

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "feedback" not in st.session_state:
    st.session_state.feedback = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

# -------------------------------
# Resume
# -------------------------------

resume = st.text_area(
    "📄 Paste Resume",
    height=220
)

# -------------------------------
# Job Description
# -------------------------------

job_description = st.text_area(
    "💼 Paste Job Description",
    height=220
)

# -------------------------------
# Generate Questions
# -------------------------------

if st.button("🚀 Generate Interview Questions"):

    if resume.strip() == "" or job_description.strip() == "":
        st.warning("Please enter Resume and Job Description.")

    else:

        with st.spinner("Generating Questions..."):

            questions = generate_questions(
                resume,
                job_description
            )

            st.session_state.questions = questions

            st.session_state.answers = [
                "" for _ in questions
            ]

            st.session_state.feedback = [
                "" for _ in questions
            ]

            st.session_state.current_question = 0

        st.success("Interview Questions Generated!")

# -------------------------------
# Interview
# -------------------------------

if len(st.session_state.questions) > 0:

    total = len(st.session_state.questions)
    current = st.session_state.current_question

    st.progress((current + 1) / total)

    st.subheader(
        f"Question {current + 1} of {total}"
    )

    question = st.session_state.questions[current]

    st.write(question)

    answer = st.text_area(
        "✍️ Your Answer",
        value=st.session_state.answers[current],
        key=f"answer_{current}",
        height=200
    )

    st.session_state.answers[current] = answer

    col1, col2, col3 = st.columns(3)
        # -------------------------------
    # Evaluate Answer
    # -------------------------------

    with col1:

        if st.button("🤖 Evaluate Answer"):

            if answer.strip() == "":
                st.warning("Please write your answer first.")

            else:

                with st.spinner("Evaluating Answer..."):

                    feedback = evaluate_answer(
                        question,
                        answer
                    )

                    st.session_state.feedback[current] = feedback

                st.rerun()

    # -------------------------------
    # Previous Button
    # -------------------------------

    with col2:

        if st.button("⬅ Previous"):

            if current > 0:
                st.session_state.current_question -= 1
                st.rerun()

    # -------------------------------
    # Next / Finish Button
    # -------------------------------

    with col3:

        if current < total - 1:

            if st.button("Next ➡"):
                st.session_state.current_question += 1
                st.rerun()

        else:

            if st.button("🏁 Finish Interview"):
                st.balloons()
                st.success("🎉 Interview Completed!")

    # -------------------------------
    # Feedback
    # -------------------------------

    if st.session_state.feedback[current] != "":

        st.divider()
        st.subheader("⭐ AI Feedback")
        st.write(st.session_state.feedback[current])

    # -------------------------------
    # Completion Summary
    # -------------------------------

    if (
        current == total - 1
        and all(f.strip() != "" for f in st.session_state.feedback)
    ):

        st.divider()
        st.header("🎉 Interview Summary")

        st.success("You completed all interview questions.")

        st.metric(
            "Questions Answered",
            f"{total}/{total}"
        )
        st.divider()


        st.header("📜 Interview History")

        for i in range(total):
            st.subheader(f"Question {i+1}")
            st.write("**Question:**")
            st.write(st.session_state.questions[i])
            st.write("**Your Answer:**")
            st.write(st.session_state.answers[i])
            st.write("**AI Feedback:**")
            st.write(st.session_state.feedback[i])
            st.divider()

        report = "AI INTERVIEW REPORT\n\n"
        for i in range(total):
            report += f"Question {i+1}\n"
            report += st.session_state.questions[i] + "\n\n"
            report += "Answer:\n" + st.session_state.answers[i] + "\n\n"
            report += "Feedback:\n" + st.session_state.feedback[i] + "\n\n"
            report += "-"*60 + "\n\n"

        st.download_button(
            "📥 Download Interview Report",
            report,
            file_name="AI_Interview_Report.txt",
            mime="text/plain"
        )

        if st.button("🔄 Start New Interview"):
            st.session_state.questions=[]
            st.session_state.answers=[]
            st.session_state.feedback=[]
            st.session_state.current_question=0
            st.rerun()
