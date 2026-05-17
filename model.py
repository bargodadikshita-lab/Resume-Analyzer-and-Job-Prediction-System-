import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from utils import extract_text, extract_skills, assign_role


def train_model(resume_folder):

    if not os.path.exists(resume_folder):
        raise FileNotFoundError(f"Folder '{resume_folder}' not found")

    data = []

    for file in os.listdir(resume_folder):
        if file.endswith(".docx"):
            file_path = os.path.join(resume_folder, file)

            text = extract_text(file_path)
            if not text:
                continue

            skills = extract_skills(text)
            role = assign_role(skills)

            data.append({
                "text": text,
                "role": role
            })

    df = pd.DataFrame(data)

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["role"], test_size=0.2, random_state=42
    )

    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)

    print(f"Model Accuracy: {acc*100:.2f}%")

    return model, vectorizer