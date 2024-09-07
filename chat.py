import numpy as np
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

# Simulated storage for content and embeddings
stored_content = {}
embeddings = {}
model = SentenceTransformer("all-MiniLM-L6-v2")  # Load a pre-trained model


@app.route("/chat", methods=["POST"])
def chat():
    if (
        not request.json
        or "chat_id" not in request.json
        or "question" not in request.json
    ):
        return jsonify({"message": "chat_id and question are required"}), 400

    chat_id = request.json["chat_id"]
    question = request.json["question"]

    if chat_id not in stored_content:
        return jsonify({"message": "Invalid chat_id"}), 404

    # Get the stored content and its embedding
    content = stored_content[chat_id]
    content_embedding = embeddings[chat_id]

    # Generate the embedding for the user's question
    question_embedding = model.encode(question, convert_to_tensor=True)

    # Calculate cosine similarities
    cosine_scores = util.pytorch_cos_sim(question_embedding, content_embedding)

    # Find the most relevant section (assuming content is split into sections)
    best_idx = np.argmax(cosine_scores.numpy())
    response = content[best_idx]  # Get the most relevant response

    return jsonify({"response": response})


# Function to simulate storing content and embeddings
def store_content(chat_id, text):
    sections = text.split(". ")  # Split text into sections based on sentences
    stored_content[chat_id] = sections
    embeddings[chat_id] = model.encode(sections, convert_to_tensor=True)


if __name__ == "_main_":
    # Example of storing content (this should be done in your process_url function)
    example_chat_id = "1"
    example_text = "This is the first sentence. This is the second sentence. The main idea of the document is..."
    store_content(example_chat_id, example_text)

    app.run(debug=True)
