from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import numpy as np
import json

app = Flask(__name__)

# Enable CORS for all origins
CORS(app, resources={r"/*": {"origins": "*"}})

# Load meme features from the JSON file
with open("memes_features.json", "r") as f:
    memes_data = json.load(f)

def find_best_match(user_encoding):
    best_match = None
    min_distance = float('inf')

    for meme_name, meme_encoding in memes_data.items():
        meme_encoding = np.array(meme_encoding)
        distance = np.linalg.norm(user_encoding - meme_encoding)
        if distance < min_distance:
            min_distance = distance
            best_match = meme_name

    return best_match

@app.route("/match", methods=["POST"])
def match_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400

    image = face_recognition.load_image_file(file)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400

    user_encoding = face_encodings[0]
    best_match = find_best_match(user_encoding)

    response = jsonify({"matched_meme": best_match} if best_match else {"error": "No match found"})
    
    # Add CORS headers manually
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


















# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import face_recognition
# import numpy as np
# import json

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "https://ai-meme-matcher.netlify.app"}})


# # Load meme features from the JSON file
# with open("memes_features.json", "r") as f:
#     memes_data = json.load(f)

# def find_best_match(user_encoding):
#     """
#     Compare the user's facial features with all meme features and return the closest match.
#     """
#     best_match = None
#     min_distance = float('inf')

#     for meme_name, meme_encoding in memes_data.items():
#         # Convert JSON list back to numpy array
#         meme_encoding = np.array(meme_encoding)
#         # Calculate the Euclidean distance between the user's encoding and the meme's encoding
#         distance = np.linalg.norm(user_encoding - meme_encoding)
#         if distance < min_distance:
#             min_distance = distance
#             best_match = meme_name

#     return best_match

# @app.route("/match", methods=["POST"])
# def match_image():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "Empty file"}), 400

#     # Load the uploaded image
#     image = face_recognition.load_image_file(file)
#     # Extract facial features (embeddings)
#     face_encodings = face_recognition.face_encodings(image)

#     if len(face_encodings) == 0:
#         return jsonify({"error": "No face detected"}), 400

#     user_encoding = face_encodings[0]
#     # Find the best matching meme
#     best_match = find_best_match(user_encoding)

#     if best_match:
#         return jsonify({"matched_meme": best_match})
#     else:
#         return jsonify({"error": "No match found"}), 404

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)

    