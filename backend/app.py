from flask import Flask, request, jsonify
from flask_cors import CORS
from database import FirestoreDB
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing

# Initialize Firestore Database
db = FirestoreDB()

@app.route('/api/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        user_text = data.get('text')
        if not user_text:
            return jsonify({"error": "Text is required"}), 400
        
        processed_text = user_text.upper()
        logger.info(f"Processed text: {processed_text}")

        # Save to Firestore
        entry = db.create_entry(user_text, processed_text)

        return jsonify({"id": entry['id'], "original": user_text, "processed": processed_text}), 201
    except Exception as e:
        logger.error(f"Error in /api/submit: {e}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = db.read_all_entries()
        return jsonify(history), 200
    except Exception as e:
        logger.error(f"Error in /api/history: {e}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/api/history/<entry_id>', methods=['PUT'])
def update_entry(entry_id):
    try:
        data = request.json
        new_text = data.get('text')
        if not new_text:
            return jsonify({"error": "Text is required"}), 400
        
        processed_text = new_text.upper()
        updated_entry = db.update_entry(entry_id, new_text, processed_text)

        return jsonify(updated_entry), 200
    except Exception as e:
        logger.error(f"Error in /api/history/<entry_id>: {e}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/api/history/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        db.delete_entry(entry_id)
        return jsonify({"message": "Entry deleted"}), 200
    except Exception as e:
        logger.error(f"Error in /api/history/<entry_id>: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
