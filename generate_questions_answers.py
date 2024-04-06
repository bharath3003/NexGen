from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")

# Set the padding token to the EOS token and specify padding side
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right" # Padding on the right side as recommended for GPT-2

# Define the text variable
input_text = """
Belgium is a small country in Europe, smaller in area than the state of Haryana. It has borders
with France, the Netherlands, Germany and Luxembourg.
"""

# Function to generate questions
def generate_questions(text):
    # Encode the input text with attention mask and padding
    inputs = tokenizer.encode_plus(text, return_tensors='pt', padding='max_length', max_length=128, truncation=True)
    # Generate questions with a more explicit and structured prompt
    prompt = "Generate a question about Belgium based on the following text: " + text
    prompt_inputs = tokenizer.encode_plus(prompt, return_tensors='pt', padding='max_length', max_length=128, truncation=True)
    # Generate questions with a higher max_new_tokens value and no_repeat_ngram_size
    questions = model.generate(prompt_inputs['input_ids'], attention_mask=prompt_inputs['attention_mask'], max_new_tokens=100, do_sample=True, temperature=0.7, no_repeat_ngram_size=2)
    # Decode the generated questions
    generated_questions = [tokenizer.decode(question, skip_special_tokens=True) for question in questions]
    return generated_questions

# Function to generate answers
def generate_answers(questions, text):
    answers = {}
    for question in questions:
        # Encode the question and context with attention mask and padding
        inputs = tokenizer.encode_plus(question + tokenizer.eos_token + text, return_tensors='pt', padding='max_length', max_length=128, truncation=True)
        # Generate answer
        answer_ids = model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], max_new_tokens=60, do_sample=True, temperature=0.7)
        # Decode the generated answer
        answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)
        answers[question] = answer
    return answers

# Main function to generate question paper
def generate_question_paper(input_text):
    questions = generate_questions(input_text)
    answers = generate_answers(questions, input_text)
    return questions, answers

# Example usage
questions, answers = generate_question_paper(input_text)
for question, answer in zip(questions, answers.values()):
    print(f"Question: {question}\nAnswer: {answer}\n")
