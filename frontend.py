import streamlit as st
from sentence_transformers import SentenceTransformer, util

# Load the pre-trained SentenceBERT model
model = SentenceTransformer('all-mpnet-base-v2')

# Function to read questions and answers from file
def read_questions_answers(filename):
    questions_answers = {"Easy": {}, "Medium": {}, "Hard": {}}
    current_difficulty = None
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#'):
                # Extract difficulty level from the line
                current_difficulty = line.split(' ')[1]
            elif line:
                # Split the line into question and answer
                parts = line.split(';')
                if len(parts) == 2:
                    question, answer = parts
                    question = question.strip()
                    answer = answer.strip()
                    
                    # Append question and answer to the respective difficulty level
                    if current_difficulty:
                        questions_answers[current_difficulty][question] = answer
                else:
                    print(f"Skipping line: {line}. Expected format: 'question;answer'")
                
    return questions_answers

# Function to calculate similarity between two texts
def get_similarity(original_text, new_text):
    original_embedding = model.encode(original_text)
    new_embedding = model.encode(new_text)
    cosine_similarity = util.pytorch_cos_sim(original_embedding, new_embedding)
    similarity_score = cosine_similarity.data.cpu().numpy()[0]
    return similarity_score

# Main function to render the app
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['See Profile', 'Practice Questions', 'Question Paper'])
    
    if page == 'See Profile':
        st.title('User Profile')
        # Add your profile details here
    
    elif page == 'Practice Questions':
        st.title('Practice Questions')
        difficulty_level = st.selectbox('Select difficulty level:', ['Easy', 'Medium', 'Hard'])

        # Load questions and answers from file
        filename = "questions_answers.txt"
        questions_answers = read_questions_answers(filename)

        # Display the selected difficulty level
        st.write(f"**Difficulty Level:** {difficulty_level}")

        # Initialize score variable
        score = 0

        # Store user answers and similarity scores
        user_answers = []
        similarity_scores = []

        # Display questions and answer section
        for i, (question, answer) in enumerate(questions_answers[difficulty_level].items()):
            st.write(f"**Question {i+1}:** {question}")
            user_answer = st.text_input(label="Your Answer:", key=f"answer_{i}")  # Unique key for each text input
            user_answers.append(user_answer)
            similarity_scores.append(get_similarity(answer, user_answer))

        if st.button("Submit Answers"):
            # Calculate score
            score = sum(score == 1.0 for score in similarity_scores)
            st.write(f"**Your Score:** {score}/{len(questions_answers[difficulty_level])}")

    elif page == 'Question Paper':
        st.title('Question Paper')
        # Implement the question paper generation here

if __name__ == "__main__":
    main()
