import face_recognition
import os
import json

# Folder containing meme images
memes_folder = "memes"
# Dictionary to store meme features
memes_data = {}

# Loop through all meme images
for filename in os.listdir(memes_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(memes_folder, filename)
        image = face_recognition.load_image_file(image_path)
        # Extract facial features (embeddings)
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            memes_data[filename] = face_encodings[0].tolist()

# Save features to a JSON file
with open("memes_features.json", "w") as f:
    json.dump(memes_data, f)

print("Features extracted and saved to memes_features.json")