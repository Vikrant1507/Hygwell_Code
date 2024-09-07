import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

# Simulated storage for processed content
stored_content = {}


@app.route("/process_url", methods=["POST"])
def process_url():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"message": "URL is required"}), 400

    try:
        # Scrape the content from the specified URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, "html.parser")

        # Clean the content (for example, extracting text)
        cleaned_content = soup.get_text(separator=" ", strip=True)

        # Generate a unique chat_id (for simplicity, using the length of stored_content)
        chat_id = str(len(stored_content) + 1)

        # Store the cleaned content with the unique chat_id
        stored_content[chat_id] = cleaned_content

        return jsonify(
            {
                "chat_id": chat_id,
                "message": "URL content processed and stored successfully.",
            }
        )

    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Error processing URL: {str(e)}"}), 500


if __name__ == "_main_":
    app.run(debug=True)
