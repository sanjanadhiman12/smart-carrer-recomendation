"""
app.py
------
Main Flask application for the Smart Career Recommendation System.

WHAT THIS FILE DOES:
    1. Loads the trained ML model (career_model.pkl).
       If the model file does not exist yet, it automatically trains
       one first by calling model_training.py.
    2. Serves the single-page website (Home / About / Features /
       Prediction Form / Contact) from templates/index.html.
    3. Handles the prediction form submission (/predict route):
         - Reads form data
         - Encodes it using the SAME encoders used during training
         - Runs it through the trained Random Forest model
         - Passes the recommended career + extra info to result.html
    4. Handles the contact form submission (/contact route).

Run with:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os
import pickle

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash

from career_info import CAREER_INFO

# ---------------------------------------------------------
# App setup
# ---------------------------------------------------------
app = Flask(__name__)
app.secret_key = "career-recommendation-secret-key"  # needed for flash messages

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "career_model.pkl")


# ---------------------------------------------------------
# STEP 1: Load (or train) the Machine Learning model
# ---------------------------------------------------------
def load_model():
    """Loads career_model.pkl. If it doesn't exist, trains it first."""
    if not os.path.exists(MODEL_PATH):
        print("No saved model found. Training a new one...")
        from model_training import train_and_save_model
        return train_and_save_model()

    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


model_bundle = load_model()
model = model_bundle["model"]
encoders = model_bundle["encoders"]
FEATURE_COLUMNS = model_bundle["feature_columns"]
CATEGORICAL_COLUMNS = model_bundle["categorical_columns"]
TARGET_COLUMN = model_bundle["target_column"]
MODEL_ACCURACY = model_bundle.get("accuracy", None)

# Dropdown options shown on the form come straight from the encoders,
# so the form and the model always stay in sync.
GENDER_OPTIONS = list(encoders["Gender"].classes_)
INTEREST_OPTIONS = list(encoders["Interest"].classes_)
PERSONALITY_OPTIONS = list(encoders["Personality Type"].classes_)
SUBJECT_OPTIONS = list(encoders["Preferred Subject"].classes_)


# ---------------------------------------------------------
# Helper: turn form data into a model-ready feature row
# ---------------------------------------------------------
def build_feature_row(form):
    """Reads the submitted form and returns a list of encoded feature
    values in the exact order the model expects (FEATURE_COLUMNS)."""

    raw_values = {
        "Gender": form.get("gender"),
        "Age": int(form.get("age")),
        "Academic Percentage": float(form.get("academic")),
        "Maths Score": float(form.get("maths")),
        "Science Score": float(form.get("science")),
        "English Score": float(form.get("english")),
        "Programming Skill": int(form.get("programming")),
        "Communication Skill": int(form.get("communication")),
        "Logical Thinking": int(form.get("logical")),
        "Creativity": int(form.get("creativity")),
        "Leadership": int(form.get("leadership")),
        "Interest": form.get("interest"),
        "Personality Type": form.get("personality"),
        "Preferred Subject": form.get("subject"),
    }

    row = []
    for col in FEATURE_COLUMNS:
        value = raw_values[col]
        if col in CATEGORICAL_COLUMNS:
            # Use the same LabelEncoder that was fit during training
            value = encoders[col].transform([value])[0]
        row.append(value)

    return row, raw_values


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------
@app.route("/")
def home():
    """Single-page site: Home, About, Features, Prediction Form, Contact."""
    return render_template(
        "index.html",
        gender_options=GENDER_OPTIONS,
        interest_options=INTEREST_OPTIONS,
        personality_options=PERSONALITY_OPTIONS,
        subject_options=SUBJECT_OPTIONS,
        model_accuracy=MODEL_ACCURACY,
    )


@app.route("/predict", methods=["POST"])
def predict():
    """Handles the career prediction form submission."""
    try:
        student_name = request.form.get("name", "Student")
        feature_row, raw_values = build_feature_row(request.form)

        # Build a single-row DataFrame with the same column names used
        # during training, so the model receives input in the format it expects
        X_input = pd.DataFrame([feature_row], columns=FEATURE_COLUMNS)

        # Predict the career (encoded number) + probability for every class
        predicted_encoded = model.predict(X_input)[0]
        probabilities = model.predict_proba(X_input)[0]

        target_encoder = encoders[TARGET_COLUMN]
        predicted_career = target_encoder.inverse_transform([predicted_encoded])[0]
        match_percentage = round(max(probabilities) * 100, 2)

        # Build a ranked list of the top 3 careers for extra insight
        career_names = target_encoder.classes_
        ranked = sorted(zip(career_names, probabilities), key=lambda x: x[1], reverse=True)
        top_matches = [{"career": c, "score": round(p * 100, 2)} for c, p in ranked[:3]]

        info = CAREER_INFO.get(predicted_career, {
            "required_skills": [],
            "future_scope": "",
            "learning_path": [],
        })

        return render_template(
            "result.html",
            student_name=student_name,
            predicted_career=predicted_career,
            match_percentage=match_percentage,
            required_skills=info["required_skills"],
            future_scope=info["future_scope"],
            learning_path=info["learning_path"],
            top_matches=top_matches,
            raw_values=raw_values,
        )

    except Exception as e:
        flash(f"Something went wrong while predicting: {e}")
        return redirect(url_for("home"))


@app.route("/contact", methods=["POST"])
def contact():
    """Handles the contact form submission (demo only - just shows a thank-you message)."""
    name = request.form.get("contact_name", "")
    email = request.form.get("contact_email", "")
    message = request.form.get("contact_message", "")

    # In a real project you would email/save this to a database.
    # For this beginner-friendly demo, we just print it to the console.
    print(f"New contact message from {name} ({email}): {message}")

    flash("Thanks for reaching out! We will get back to you soon.")
    return redirect(url_for("home") + "#contact")


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
