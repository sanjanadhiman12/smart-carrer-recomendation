# Smart Career Recommendation System

An AI-powered web application that recommends a suitable career to a
student based on their academics, skills, interests, and personality
type. Built as a beginner-friendly final-year Computer Science project.

**Tagline:** Discover Your Skills • Choose the Right Career • Build Your Future

<img width="1024" height="1536" alt="smart_career_recommendation_system" src="https://github.com/user-attachments/assets/22f19b32-3d2c-4117-8518-9a7340538bf0" />


---

## Tech Stack

| Layer            | Technology                          |
|-------------------|--------------------------------------|
| Frontend          | HTML5, CSS3, JavaScript              |
| Backend           | Python, Flask                        |
| Machine Learning  | Pandas, NumPy, Scikit-learn          |
| Model             | Random Forest Classifier             |
| Model Persistence | Pickle (`career_model.pkl`)          |

---

## Project Structure

```
Smart-Career-Recommendation-System/
│── app.py                 # Flask web application (routes + prediction logic)
│── model_training.py      # Trains the Random Forest model and saves it as .pkl
│── generate_dataset.py    # Creates the synthetic career_dataset.csv
│── career_info.py         # Required skills / future scope / learning path per career
│── career_dataset.csv     # Training dataset (1500 student records)
│── career_model.pkl       # Saved trained model + encoders (auto-generated)
│── requirements.txt       # Python dependencies
│── templates/
│   ├── index.html         # Home, About, Features, Prediction Form, Contact
│   └── result.html        # Prediction result page
│── static/
│   ├── style.css          # Blue / Purple / Cyan themed styling
│   ├── script.js          # Client-side interactivity
│   └── images/
```

---

## How It Works

1. **Dataset** — `career_dataset.csv` contains 1,500 synthetic student
   records with 14 input features (Gender, Age, Academic %, Maths/Science/
   English scores, Programming/Communication/Logical/Creativity/Leadership
   skills, Interest, Personality Type, Preferred Subject) and a target
   `Career Label` across 10 careers.

2. **Training (`model_training.py`)**
   - Loads and cleans the dataset
   - Label-encodes all categorical columns
   - Splits data into train/test sets (80/20)
   - Trains a `RandomForestClassifier`
   - Evaluates it with **Accuracy Score** and a **Confusion Matrix**
   - Saves the model + encoders together into `career_model.pkl` using `pickle`

3. **Web App (`app.py`)**
   - Loads `career_model.pkl` on startup (auto-trains if the file is missing)
   - Serves the single-page site (`index.html`) with Home, About, Features,
     the Prediction Form, and Contact sections
   - On form submission (`/predict`), encodes the input the same way as
     training, runs it through the model, and renders `result.html` with:
     - Recommended Career
     - Career Match Percentage (from `predict_proba`)
     - Required Skills
     - Future Scope
     - Suggested Learning Path
     - Top 3 career matches with confidence bars

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Regenerate the dataset
python generate_dataset.py

# 3. Train the model (creates career_model.pkl)
python model_training.py

# 4. Run the Flask app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

> Note: If `career_model.pkl` doesn't exist yet, `app.py` will train it
> automatically the first time you run it, so steps 2-3 are optional.

---

## Model Performance

The Random Forest Classifier achieves roughly **70-75% accuracy** on the
held-out test set across 10 balanced career classes — solid performance
for a synthetic dataset with 8 numeric + 4 categorical features and
realistic overlap between related careers (e.g., Software Engineer vs.
Data Scientist).

---

## Notes for Students / Presenters

- The dataset is synthetically generated (`generate_dataset.py`) using
  realistic per-career statistical profiles, so it's free to use, modify,
  and regenerate for demos.
- All code is commented step-by-step to make it easy to explain during a
  viva/project defense.
- To add a new career: add its profile to `CAREER_PROFILES` in
  `generate_dataset.py` and its info to `CAREER_INFO` in `career_info.py`,
  then regenerate the dataset and retrain.
