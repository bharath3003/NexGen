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
    st.title('Personalized Learning Platform')
    st.subheader('Tailored Question Papers')
    
    # Load questions and answers from file
    filename = "questions_answers.txt"
    questions_answers = read_questions_answers(filename)
    
    # Display dropdown for selecting difficulty level
    difficulty_level = st.selectbox('Select difficulty level:', ['Easy', 'Medium', 'Hard'])
    
    # Display the selected difficulty level
    st.write(f"**Difficulty Level:** {difficulty_level}")
    
    # Display dropdown for selecting question
    selected_question = st.selectbox('Select question:', list(questions_answers[difficulty_level].keys()))
    
    # Display the selected question
    st.write(f"**Question:** {selected_question}")
    
    # Input field for student's answer
    user_answer = st.text_input(label="Your Answer:")
    if st.button("Check Similarity"):
        correct_answer = questions_answers[difficulty_level].get(selected_question, "")
        similarity_score = get_similarity(correct_answer, user_answer)
        st.write(f"Similarity with correct answer: {similarity_score}")

if __name__ == "__main__":
    main()
