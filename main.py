from flask import Flask, request, render_template
import os
os.makedirs("uploads", exist_ok=True)
os.makedirs("resumes", exist_ok=True)
from utils import extract_text, extract_skills
from model import train_model

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("Training model... please wait")
model, vectorizer = train_model("resumes")
print("Model trained successfully")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    uploaded_file = request.files.get("resume")

    if not uploaded_file:
        return "No file uploaded", 400

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)

    # Extract text and skills
    text = extract_text(file_path)
    skills = extract_skills(text)

    # Model prediction
    text_vector = vectorizer.transform([text])
    predicted_role = model.predict(text_vector)[0]

    # Confidence score
    try:
        confidence = max(model.predict_proba(text_vector)[0]) * 100
    except:
        confidence = 0

    # Debug output (check terminal)
    print("\n----- DEBUG INFO -----")
    print("Extracted Skills:", skills)
    print("Prediction before override:", predicted_role)

    # Override logic for ML roles
    ml_skills = {"machine learning", "nlp", "deep learning", "pandas", "numpy", "scikit-learn"}

    if len(ml_skills & set(skills)) >= 2:
        predicted_role = "Data Scientist"

    print("Prediction after override:", predicted_role)
    print("----------------------\n")

    return render_template(
        "result.html",
        role=predicted_role,
        skills=skills,
        confidence=round(confidence, 2)
    )


if __name__ == "__main__":
    app.run(debug=True)