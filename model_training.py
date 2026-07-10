"""
model_training.py
------------------
Beginner-friendly ML training script for the
Smart Career Recommendation System.

STEPS PERFORMED IN THIS FILE:
    1. Load the dataset (career_dataset.csv)
    2. Clean / preprocess the data
    3. Label-encode all categorical (text) columns
    4. Split data into training and testing sets
    5. Train a Random Forest Classifier
    6. Evaluate the model (accuracy + confusion matrix)
    7. Save the trained model + encoders to career_model.pkl using pickle

Run this file directly to (re)train the model:
    python model_training.py

app.py will automatically call this file if career_model.pkl
does not already exist.
"""

import os
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ---------------------------------------------------------
# File locations
# ---------------------------------------------------------
DATASET_PATH = os.path.join(os.path.dirname(__file__), "career_dataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "career_model.pkl")

# Columns that contain TEXT (categorical) data and need Label Encoding
CATEGORICAL_COLUMNS = [
    "Gender",
    "Interest",
    "Personality Type",
    "Preferred Subject",
]

TARGET_COLUMN = "Career Label"

# The exact order of columns the model expects as input.
# app.py must build a row in this SAME order when predicting.
FEATURE_COLUMNS = [
    "Gender",
    "Age",
    "Academic Percentage",
    "Maths Score",
    "Science Score",
    "English Score",
    "Programming Skill",
    "Communication Skill",
    "Logical Thinking",
    "Creativity",
    "Leadership",
    "Interest",
    "Personality Type",
    "Preferred Subject",
]


def train_and_save_model():
    """Loads the dataset, trains a Random Forest model and saves it as a .pkl file."""

    # ---------------------------------------------------------
    # STEP 1: Load Dataset
    # ---------------------------------------------------------
    if not os.path.exists(DATASET_PATH):
        # If the dataset is missing, build it automatically using our
        # synthetic data generator so the project still works out of the box.
        from generate_dataset import generate_dataset
        df = generate_dataset()
        df.to_csv(DATASET_PATH, index=False)
    else:
        df = pd.read_csv(DATASET_PATH)

    print("Dataset loaded successfully. Shape:", df.shape)

    # ---------------------------------------------------------
    # STEP 2: Basic Data Cleaning / Preprocessing
    # ---------------------------------------------------------
    # Drop any completely empty rows, just in case
    df = df.dropna()

    # ---------------------------------------------------------
    # STEP 3: Label Encoding of categorical columns
    # ---------------------------------------------------------
    # We keep a dictionary of encoders so app.py can reuse the SAME
    # encoding scheme when it receives new form data from the user.
    encoders = {}

    for column in CATEGORICAL_COLUMNS:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        encoders[column] = le

    # Encode the target (Career Label) column too
    target_encoder = LabelEncoder()
    df[TARGET_COLUMN] = target_encoder.fit_transform(df[TARGET_COLUMN])
    encoders[TARGET_COLUMN] = target_encoder

    # ---------------------------------------------------------
    # STEP 4: Train-Test Split
    # ---------------------------------------------------------
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ---------------------------------------------------------
    # STEP 5: Train the Random Forest Classifier
    # ---------------------------------------------------------
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # ---------------------------------------------------------
    # STEP 6: Evaluate the Model
    # ---------------------------------------------------------
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("\n--- MODEL EVALUATION ---")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(
        classification_report(
            y_test, y_pred, target_names=target_encoder.classes_
        )
    )

    # ---------------------------------------------------------
    # STEP 7: Save the trained model + encoders using Pickle
    # ---------------------------------------------------------
    model_bundle = {
        "model": model,
        "encoders": encoders,
        "feature_columns": FEATURE_COLUMNS,
        "categorical_columns": CATEGORICAL_COLUMNS,
        "target_column": TARGET_COLUMN,
        "accuracy": accuracy,
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model_bundle, f)

    print(f"\nModel saved successfully -> {MODEL_PATH}")
    return model_bundle


if __name__ == "__main__":
    train_and_save_model()
