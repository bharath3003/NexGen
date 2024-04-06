from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-mpnet-base-v2')

from sentence_transformers import SentenceTransformer, util

# Load the pre-trained SentenceBERT model (assuming it's already loaded)
# model = SentenceTransformer('all-mpnet-base-v2')

def get_similarity(original_text, new_text):
  # Encode the sentences into vectors
  original_embedding = model.encode(original_text)
  new_embedding = model.encode(new_text)

  # Calculate cosine similarity between the embeddings
  cosine_similarity = util.pytorch_cos_sim(original_embedding, new_embedding)
  similarity_score = cosine_similarity.data.cpu().numpy()[0]

  # Define your rating scale (modify as needed)
  rating_scale = {
      0.9: "Very similar",
      0.8: "Similar",
      0.7: "Somewhat similar",
      0.6: "Neutral",
      0.5: "Less similar" 
  }

  # Get the rating based on the similarity score
  for threshold, rating in rating_scale.items():
    if similarity_score >= threshold:  # Direct comparison with float threshold
      return rating

  # Handle cases where score falls below the lowest threshold
  return rating_scale[list(rating_scale.keys())[-1]]

# Example usage
original_text = "The weather is pleasant today."
new_text1 = "It's a beautiful day outside."  # Similar
new_text2 = "The rain is pouring heavily."  # Less similar

similarity_score1 = get_similarity(original_text, new_text1)
similarity_score2 = get_similarity(original_text, new_text2)

print(f"Similarity between '{original_text}' and '{new_text1}': {similarity_score1}")
print(f"Similarity between '{original_text}' and '{new_text2}': {similarity_score2}")
