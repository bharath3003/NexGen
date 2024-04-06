import streamlit as st
from sentence_transformers import SentenceTransformer, util

# Load the pre-trained SentenceBERT model
model = SentenceTransformer('all-mpnet-base-v2')

# Function to read questions and answers from file based on difficulty level
def read_questions_answers(difficulty_level):
    filename = f"{difficulty_level.lower()}.txt"
    questions_answers = {}

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(';')
                if len(parts) == 2:
                    question, answer = parts
                    question = question.strip()
                    answer = answer.strip()
                    questions_answers[question] = answer
                else:
                    print(f"Skipping line: {line}. Expected format: 'question;answer'")

    return questions_answers

# Function to calculate similarity between two texts
def get_similarity(original_text, new_text):
    if not new_text:  # Check if user answer is empty
        return 0.0  # Return 0 similarity
    original_embedding = model.encode(original_text)
    new_embedding = model.encode(new_text)
    cosine_similarity = util.pytorch_cos_sim(original_embedding, new_embedding)
    similarity_score = cosine_similarity.data.cpu().numpy()[0]
    return similarity_score

# Main function to render the app
def main():
    st.title('Practice Questions')
    difficulty_level = st.selectbox('Select difficulty level:', ['Easy', 'Medium', 'Hard'])

    # Load questions and answers from file based on selected difficulty level
    questions_answers = read_questions_answers(difficulty_level)

    # Display the selected difficulty level
    st.write(f"**Difficulty Level:** {difficulty_level}")

    # Initialize score and similarity_scores variables
    score = 0
    similarity_scores = []

    # Clear session_state for user_answers when switching difficulty levels
    if 'difficulty_level' in st.session_state and st.session_state['difficulty_level'] != difficulty_level:
        st.session_state['user_answers'] = [""] * 5

    st.session_state['difficulty_level'] = difficulty_level

    # Store user answers and similarity scores using st.session_state
    if 'user_answers' not in st.session_state:
        st.session_state['user_answers'] = [""] * 5  # Initialize with 5 empty answers

    # Display questions and answer section
    for i, (question, answer) in enumerate(list(questions_answers.items())[:5]):  # Display only 5 questions
        st.write(f"**Question {i+1}:** {question}")
        user_answer = st.text_input(label="Your Answer:", key=f"answer_{i}",
                                    value=st.session_state['user_answers'][i])  # Get answer from session_state
        st.session_state['user_answers'][i] = user_answer  # Update session_state

    if st.button("Submit Answers"):
        # Calculate similarity scores and display correct answers
        for i, (question, answer) in enumerate(list(questions_answers.items())[:5]):
            similarity_scores.append(get_similarity(answer, st.session_state['user_answers'][i]))
            st.write(f"**Question {i+1}:** {question}")
            st.write(f"**Your Answer:** {st.session_state['user_answers'][i]}")
            st.write(f"**Correct Answer:** {answer}")
            st.write("--------")

        # Calculate score out of 5
        score = sum(score == 1.0 for score in similarity_scores)
        score = min(5, max(0, score * 5))  # Limit score to be between 0 and 5 without rounding
        st.write(f"**Your Score:** {score}/5")

if __name__ == "__main__":
    main()