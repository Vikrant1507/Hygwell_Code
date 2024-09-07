import os
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader

app = Flask(__name__)

# Simulated storage for processed content
stored_content = {}

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    if "pdf_file" not in request.files:
        return jsonify({"message": "PDF file is required"}), 400

    pdf_file = request.files["pdf_file"]

    if pdf_file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_file.filename)
    pdf_file.save(file_path)

    try:
        # Extract text from the PDF
        reader = PdfReader(file_path)
        text = "".join([page.extract_text() for page in reader.pages])

        # Clean the text (for example, removing extra spaces and line breaks)
        cleaned_text = " ".join(text.split())

        # Generate a unique chat_id (for simplicity, using the length of stored_content)
        chat_id = str(len(stored_content) + 1)

        # Store the cleaned text with the unique chat_id
        stored_content[chat_id] = cleaned_text

        # Remove the uploaded file
        os.remove(file_path)

        return jsonify(
            {
                "chat_id": chat_id,
                "message": "PDF content processed and stored successfully.",
            }
        )

    except Exception as e:
        # Remove the uploaded file in case of an error
        os.remove(file_path)
        return jsonify({"message": f"Error processing PDF: {str(e)}"}), 500


if __name__ == "_main_":
    app.run(debug=True)
