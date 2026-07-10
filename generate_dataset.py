"""
generate_dataset.py
--------------------
Beginner-friendly helper script used ONLY to create the sample
'career_dataset.csv' file that ships with this project.

You do NOT need to run this again unless you want a fresh dataset -
career_dataset.csv is already included in the project folder.

APPROACH:
Each career has a "profile" - typical ranges for scores/skills and a
set of likely interests / personality types / preferred subjects.
For every student record we first randomly choose a career, then
generate feature values that follow that career's profile (with
realistic random noise). This keeps the dataset balanced across
careers and gives the Machine Learning model clear, learnable
patterns - similar to how real-world survey/education datasets
are simulated for teaching purposes.
"""

import numpy as np
import pandas as pd

# Fix the random seed so the dataset is the same every time we run this
np.random.seed(42)

GENDERS = ["Male", "Female"]

CAREERS = [
    "Software Engineer", "Data Scientist", "Doctor", "Mechanical Engineer",
    "Civil Engineer", "Graphic Designer", "Business Analyst", "Teacher",
    "Lawyer", "Psychologist"
]

N_SAMPLES = 1500

# ---------------------------------------------------------
# Career profile definitions
# ---------------------------------------------------------
# For every career we define:
#   scores  -> (mean, std) for Academic %, Maths, Science, English
#   skills  -> (mean, std) for Programming, Communication, Logical,
#              Creativity, Leadership   (all on a 1-10 scale)
#   interests / personalities / subjects -> likely categorical choices
#              with probability weights (mostly on-profile, a little
#              off-profile noise for realism)
CAREER_PROFILES = {
    "Software Engineer": {
        "scores": {"academic": (78, 8), "maths": (82, 8), "science": (70, 10), "english": (65, 10)},
        "skills": {"programming": (9, 1), "communication": (5, 2), "logical": (8, 1.5), "creativity": (6, 2), "leadership": (5, 2)},
        "interest": {"Technology": 0.55, "Design": 0.15, "Mathematics": 0.15, "Science": 0.15},
        "personality": {"Analytical": 0.4, "Creative": 0.3, "Investigative": 0.2, "Practical": 0.1},
        "subject": {"Computer Science": 0.6, "Mathematics": 0.25, "Science": 0.15},
    },
    "Data Scientist": {
        "scores": {"academic": (82, 7), "maths": (88, 6), "science": (75, 8), "english": (65, 10)},
        "skills": {"programming": (8, 1.5), "communication": (5, 2), "logical": (9, 1), "creativity": (5, 2), "leadership": (5, 2)},
        "interest": {"Technology": 0.35, "Mathematics": 0.4, "Science": 0.25},
        "personality": {"Analytical": 0.55, "Investigative": 0.3, "Practical": 0.15},
        "subject": {"Mathematics": 0.45, "Computer Science": 0.4, "Science": 0.15},
    },
    "Doctor": {
        "scores": {"academic": (88, 6), "maths": (65, 10), "science": (90, 6), "english": (70, 10)},
        "skills": {"programming": (3, 2), "communication": (7, 1.5), "logical": (7, 1.5), "creativity": (5, 2), "leadership": (6, 2)},
        "interest": {"Medicine": 0.65, "Science": 0.25, "Social Work": 0.1},
        "personality": {"Investigative": 0.45, "Social": 0.3, "Analytical": 0.25},
        "subject": {"Biology": 0.55, "Science": 0.35, "English": 0.1},
    },
    "Mechanical Engineer": {
        "scores": {"academic": (75, 8), "maths": (80, 8), "science": (78, 8), "english": (60, 10)},
        "skills": {"programming": (5, 2), "communication": (5, 2), "logical": (8, 1.5), "creativity": (6, 2), "leadership": (5, 2)},
        "interest": {"Technology": 0.3, "Mathematics": 0.3, "Science": 0.4},
        "personality": {"Practical": 0.55, "Analytical": 0.3, "Investigative": 0.15},
        "subject": {"Mathematics": 0.45, "Science": 0.45, "Computer Science": 0.1},
    },
    "Civil Engineer": {
        "scores": {"academic": (74, 8), "maths": (78, 8), "science": (76, 8), "english": (60, 10)},
        "skills": {"programming": (3, 2), "communication": (5, 2), "logical": (7, 1.5), "creativity": (5, 2), "leadership": (6, 2)},
        "interest": {"Science": 0.4, "Mathematics": 0.35, "Technology": 0.25},
        "personality": {"Practical": 0.6, "Analytical": 0.25, "Investigative": 0.15},
        "subject": {"Science": 0.45, "Mathematics": 0.45, "Social Studies": 0.1},
    },
    "Graphic Designer": {
        "scores": {"academic": (68, 10), "maths": (55, 12), "science": (55, 12), "english": (70, 10)},
        "skills": {"programming": (4, 2), "communication": (6, 2), "logical": (5, 2), "creativity": (9, 1), "leadership": (5, 2)},
        "interest": {"Design": 0.6, "Arts": 0.3, "Technology": 0.1},
        "personality": {"Creative": 0.7, "Social": 0.15, "Practical": 0.15},
        "subject": {"Arts": 0.6, "Computer Science": 0.2, "English": 0.2},
    },
    "Business Analyst": {
        "scores": {"academic": (76, 8), "maths": (75, 9), "science": (60, 10), "english": (72, 9)},
        "skills": {"programming": (5, 2), "communication": (7, 1.5), "logical": (7, 1.5), "creativity": (5, 2), "leadership": (8, 1.5)},
        "interest": {"Business": 0.65, "Technology": 0.2, "Mathematics": 0.15},
        "personality": {"Leadership": 0.45, "Analytical": 0.35, "Social": 0.2},
        "subject": {"Commerce": 0.55, "Mathematics": 0.3, "Social Studies": 0.15},
    },
    "Teacher": {
        "scores": {"academic": (77, 8), "maths": (65, 10), "science": (65, 10), "english": (78, 8)},
        "skills": {"programming": (3, 2), "communication": (9, 1), "logical": (6, 2), "creativity": (6, 2), "leadership": (6, 2)},
        "interest": {"Social Work": 0.4, "Arts": 0.3, "Medicine": 0.1, "Business": 0.2},
        "personality": {"Social": 0.55, "Creative": 0.25, "Leadership": 0.2},
        "subject": {"English": 0.4, "Social Studies": 0.3, "Arts": 0.3},
    },
    "Lawyer": {
        "scores": {"academic": (80, 7), "maths": (60, 10), "science": (58, 10), "english": (82, 7)},
        "skills": {"programming": (2, 2), "communication": (9, 1), "logical": (7, 1.5), "creativity": (5, 2), "leadership": (8, 1.5)},
        "interest": {"Business": 0.3, "Social Work": 0.25, "Medicine": 0.05, "Technology": 0.1, "Arts": 0.3},
        "personality": {"Leadership": 0.4, "Social": 0.3, "Investigative": 0.3},
        "subject": {"English": 0.4, "Social Studies": 0.35, "Commerce": 0.25},
    },
    "Psychologist": {
        "scores": {"academic": (78, 8), "maths": (58, 10), "science": (68, 10), "english": (74, 9)},
        "skills": {"programming": (2, 2), "communication": (8, 1.5), "logical": (6, 2), "creativity": (6, 2), "leadership": (5, 2)},
        "interest": {"Medicine": 0.25, "Social Work": 0.55, "Arts": 0.2},
        "personality": {"Social": 0.55, "Investigative": 0.25, "Creative": 0.2},
        "subject": {"Biology": 0.35, "Social Studies": 0.45, "English": 0.2},
    },
}

INTERESTS = ["Technology", "Science", "Arts", "Business", "Medicine", "Social Work", "Design", "Mathematics"]
PERSONALITIES = ["Analytical", "Creative", "Social", "Leadership", "Practical", "Investigative"]
SUBJECTS = ["Mathematics", "Science", "English", "Computer Science", "Arts", "Commerce", "Biology", "Social Studies"]


def _clip(value, low, high):
    return float(np.clip(value, low, high))


def _weighted_choice(prob_dict):
    """Pick a random key from a dict of {value: probability}."""
    values = list(prob_dict.keys())
    weights = np.array(list(prob_dict.values()), dtype=float)
    weights = weights / weights.sum()
    return np.random.choice(values, p=weights)


def generate_dataset(n=N_SAMPLES):
    rows = []

    for _ in range(n):
        career = np.random.choice(CAREERS)
        profile = CAREER_PROFILES[career]

        gender = np.random.choice(GENDERS)
        age = np.random.randint(16, 23)

        s = profile["scores"]
        academic_pct = _clip(np.random.normal(*s["academic"]), 40, 99)
        maths = _clip(np.random.normal(*s["maths"]), 30, 100)
        science = _clip(np.random.normal(*s["science"]), 30, 100)
        english = _clip(np.random.normal(*s["english"]), 30, 100)

        k = profile["skills"]
        programming = int(round(_clip(np.random.normal(*k["programming"]), 1, 10)))
        communication = int(round(_clip(np.random.normal(*k["communication"]), 1, 10)))
        logical = int(round(_clip(np.random.normal(*k["logical"]), 1, 10)))
        creativity = int(round(_clip(np.random.normal(*k["creativity"]), 1, 10)))
        leadership = int(round(_clip(np.random.normal(*k["leadership"]), 1, 10)))

        # Categorical fields mostly follow the career profile, with a
        # small chance (10%) of being a totally random / off-profile
        # choice - this mimics real students who don't perfectly fit
        # a stereotype and keeps the model from overfitting.
        if np.random.rand() < 0.10:
            interest = np.random.choice(INTERESTS)
        else:
            interest = _weighted_choice(profile["interest"])

        if np.random.rand() < 0.10:
            personality = np.random.choice(PERSONALITIES)
        else:
            personality = _weighted_choice(profile["personality"])

        if np.random.rand() < 0.10:
            subject = np.random.choice(SUBJECTS)
        else:
            subject = _weighted_choice(profile["subject"])

        rows.append({
            "Gender": gender,
            "Age": age,
            "Academic Percentage": round(academic_pct, 2),
            "Maths Score": round(maths, 2),
            "Science Score": round(science, 2),
            "English Score": round(english, 2),
            "Programming Skill": programming,
            "Communication Skill": communication,
            "Logical Thinking": logical,
            "Creativity": creativity,
            "Leadership": leadership,
            "Interest": interest,
            "Personality Type": personality,
            "Preferred Subject": subject,
            "Career Label": career,
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("career_dataset.csv", index=False)
    print(f"Dataset created with {len(df)} rows -> career_dataset.csv")
    print(df["Career Label"].value_counts())
