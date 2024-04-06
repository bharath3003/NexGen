import streamlit as st

def main():
    st.title("Online Practice Exam System")

    st.markdown(
        "Welcome to the Online Practice Exam System. This platform is designed to assist students in practicing "
        "question papers of varying difficulty, getting scores, viewing a leaderboard, and accessing answer sources "
        "for incorrect answers."
    )

    st.header("Key Features")

    st.markdown(
        "- Practice Questions: Practice question papers of varying difficulty levels."
    )
    st.markdown(
        "- Score Tracking: Get scores for each practice session to monitor your progress."
    )
    st.markdown(
        "- Leaderboard: View the leaderboard to see top-performing students and your rank."
    )
    st.markdown(
        "- Answer Sources: Access sources for correct answers and explanations for incorrect answers."
    )

    st.header("How It Works")

    st.markdown(
        "1. Practice Questions: Choose a question paper from the available options."
    )
    st.markdown(
        "2. Submit Answers: Submit your answers and get instant feedback on correctness."
    )
    st.markdown(
        "3. Track Scores: Monitor your scores over time to track your progress."
    )
    st.markdown(
        "4. Leaderboard: Check the leaderboard to see how you rank among other students."
    )

if __name__ == "__main__":
    main()
