"""
career_info.py
---------------
Static reference data describing each career that the model can predict.
Kept in its own file so app.py stays clean and this content is easy to
edit/extend without touching the ML or routing logic.

Each entry contains:
    required_skills   -> list of key skills for that career
    future_scope      -> short paragraph about growth / demand
    learning_path      -> ordered list of suggested learning steps
"""

CAREER_INFO = {
    "Software Engineer": {
        "required_skills": ["Programming (Python/Java/C++)", "Data Structures & Algorithms", "Problem Solving", "Git & Version Control", "Teamwork"],
        "future_scope": "Software development remains one of the fastest-growing fields worldwide, with strong demand across web, mobile, cloud, and AI-driven applications.",
        "learning_path": [
            "Learn a core programming language (Python or Java)",
            "Master Data Structures & Algorithms",
            "Build projects using Git/GitHub",
            "Learn a web or app development framework",
            "Contribute to open-source / build a portfolio",
        ],
    },
    "Data Scientist": {
        "required_skills": ["Python/R", "Statistics & Probability", "Machine Learning", "Data Visualization", "SQL"],
        "future_scope": "Organizations increasingly rely on data-driven decisions, making data science and analytics one of the most in-demand career paths globally.",
        "learning_path": [
            "Build strong foundations in Statistics & Mathematics",
            "Learn Python libraries: Pandas, NumPy, Scikit-learn",
            "Practice on real datasets (Kaggle competitions)",
            "Learn SQL and data visualization tools",
            "Work on end-to-end ML projects",
        ],
    },
    "Doctor": {
        "required_skills": ["Biology & Medical Sciences", "Critical Thinking", "Empathy & Patient Care", "Attention to Detail", "Communication"],
        "future_scope": "Healthcare demand continues to rise steadily, offering stable, respected, and impactful career opportunities across specializations.",
        "learning_path": [
            "Excel in Biology, Chemistry and Physics (PCB)",
            "Clear medical entrance examinations (e.g., NEET)",
            "Complete MBBS and internship",
            "Choose a specialization (MD/MS)",
            "Pursue continuous medical education",
        ],
    },
    "Mechanical Engineer": {
        "required_skills": ["Mathematics & Physics", "CAD Software", "Thermodynamics", "Problem Solving", "Manufacturing Knowledge"],
        "future_scope": "Mechanical engineering remains foundational to manufacturing, automotive, robotics, and energy sectors with steady global demand.",
        "learning_path": [
            "Build a strong base in Physics & Mathematics",
            "Pursue a B.Tech/B.E. in Mechanical Engineering",
            "Learn CAD tools (AutoCAD, SolidWorks)",
            "Gain hands-on experience via internships",
            "Specialize in robotics, automotive, or energy systems",
        ],
    },
    "Civil Engineer": {
        "required_skills": ["Mathematics & Physics", "Structural Analysis", "AutoCAD/Revit", "Project Management", "Attention to Detail"],
        "future_scope": "Rapid urbanization and infrastructure development ensure consistent demand for skilled civil engineers worldwide.",
        "learning_path": [
            "Strengthen Mathematics & Physics fundamentals",
            "Pursue a B.Tech/B.E. in Civil Engineering",
            "Learn design tools like AutoCAD and Revit",
            "Gain site experience through internships",
            "Consider certifications in project management",
        ],
    },
    "Graphic Designer": {
        "required_skills": ["Creativity", "Adobe Photoshop/Illustrator", "Typography", "Color Theory", "UI/UX Basics"],
        "future_scope": "Digital content and branding needs continue to grow across industries, creating steady opportunities in design roles.",
        "learning_path": [
            "Learn design fundamentals (color, layout, typography)",
            "Master tools like Photoshop and Illustrator",
            "Build a strong design portfolio",
            "Learn UI/UX design basics",
            "Freelance or intern to gain real-world experience",
        ],
    },
    "Business Analyst": {
        "required_skills": ["Analytical Thinking", "Excel/SQL", "Communication", "Business Strategy", "Presentation Skills"],
        "future_scope": "Businesses increasingly need analysts who can translate data into strategy, keeping this role in strong demand across industries.",
        "learning_path": [
            "Build strong Excel and SQL skills",
            "Learn business fundamentals & strategy",
            "Practice case studies and data storytelling",
            "Learn a BI tool (Power BI/Tableau)",
            "Pursue relevant certifications or internships",
        ],
    },
    "Teacher": {
        "required_skills": ["Subject Expertise", "Communication", "Patience", "Classroom Management", "Curriculum Planning"],
        "future_scope": "Education remains a foundational sector with consistent demand for skilled, passionate educators at all levels.",
        "learning_path": [
            "Gain deep expertise in your chosen subject",
            "Pursue a B.Ed or relevant teaching qualification",
            "Develop communication and mentoring skills",
            "Gain classroom experience via internships",
            "Stay updated with modern teaching methods",
        ],
    },
    "Lawyer": {
        "required_skills": ["Legal Knowledge", "Communication", "Analytical Thinking", "Research Skills", "Negotiation"],
        "future_scope": "Legal expertise remains essential across business, government, and society, offering diverse and stable career paths.",
        "learning_path": [
            "Build strong reading & argumentation skills",
            "Pursue a Bachelor's degree in Law (LLB)",
            "Intern with law firms or legal professionals",
            "Specialize in a legal domain of interest",
            "Prepare for bar examinations",
        ],
    },
    "Psychologist": {
        "required_skills": ["Empathy", "Active Listening", "Research Methods", "Communication", "Critical Thinking"],
        "future_scope": "Growing awareness of mental health is driving increased demand for qualified psychologists and counselors globally.",
        "learning_path": [
            "Pursue a Bachelor's degree in Psychology",
            "Gain practical experience through internships",
            "Pursue a Master's or specialization (Clinical/Counseling)",
            "Develop strong communication and empathy skills",
            "Obtain relevant licensure/certification",
        ],
    },
}
