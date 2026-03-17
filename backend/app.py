# from flask_cors import CORS
# from flask import Flask, request, jsonify
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import re
# import fitz  # PyMuPDF

# app = Flask(__name__)
# CORS(app)

# # Clean text
# def clean_text(text):
#     text = text.lower()
#     text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
#     return text

# # Compute similarity
# def compute_similarity(resume, job_desc):
#     texts = [clean_text(resume), clean_text(job_desc)]
    
#     vectorizer = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = vectorizer.fit_transform(texts)
    
#     similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
#     return round(similarity[0][0] * 100, 2)

# # Extract skills
# # def extract_skills(text):
# #     text = text.lower()

# #     skill_map = {
# #         "aws": ["aws", "amazon web services"],
# #         "machine learning": ["machine learning", "ml"],
# #         "react": ["react", "reactjs"],
# #     }

# #     found_skills = []

# #     for skill, variants in skill_map.items():
# #         for v in variants:
# #             if v in text:
# #                 found_skills.append(skill)
# #                 break

# #     return found_skills

# def extract_skills(text, skills_list):
#     text = text.lower()
#     found_skills = []

#     for skill in skills_list:
#         if skill in text:
#             found_skills.append(skill)

#     return found_skills

# def extract_text_from_pdf(file):
#     text = ""
#     pdf = fitz.open(stream=file.read(), filetype="pdf")
    
#     for page in pdf:
#         text += page.get_text()
    
#     return text

# # API route
# @app.route("/analyze", methods=["POST"])
# def analyze():
#     skills_list = [
#     "python", "java", "react", "node", "mongodb",
#     "machine learning", "deep learning", "nlp",
#     "data analysis", "sql", "aws", "docker", "kubernetes"
# ]
#     file = request.files.get("resume")
#     job_desc = request.form.get("job_description", "")

#     if file:
#         resume = extract_text_from_pdf(file)
#     else:
#         resume = ""

#     score = compute_similarity(resume, job_desc)

#     resume_skills = extract_skills(resume, skills_list)
#     job_skills = extract_skills(job_desc, skills_list)

#     missing_skills = list(set(job_skills) - set(resume_skills))

#     return jsonify({
#         "match_score": score,
#         "resume_skills": resume_skills,
#         "missing_skills": missing_skills
#     })


# # Run server
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)

# -------------------------
# Clean Text
# -------------------------
def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# -------------------------
# Compute Similarity Score
# -------------------------
def compute_similarity(resume, job_desc):
    resume = clean_text(resume)
    job_desc = clean_text(job_desc)

    if not resume or not job_desc:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([resume, job_desc])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(float(similarity[0][0]) * 100, 2)

# -------------------------
# Extract Skills
# -------------------------
def extract_skills(text, skills_list):
    text = clean_text(text)
    found_skills = []

    for skill in skills_list:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills

# -------------------------
# Extract Text from PDF
# -------------------------
def extract_text_from_pdf(file):
    text = ""
    try:
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        pdf.close()
    except Exception:
        return ""
    return text

# -------------------------
# API Route
# -------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    skills_list = [
        "python", "java", "react", "node", "mongodb",
        "machine learning", "deep learning", "nlp",
        "data analysis", "sql", "aws", "docker", "kubernetes"
    ]

    file = request.files.get("resume")
    job_desc = request.form.get("job_description", "")

    resume = ""

    if file:
        resume = extract_text_from_pdf(file)

    # Compute score
    score = compute_similarity(resume, job_desc)

    # Extract skills
    resume_skills = extract_skills(resume, skills_list)
    job_skills = extract_skills(job_desc, skills_list)

    missing_skills = list(set(job_skills) - set(resume_skills))

    return jsonify({
        "match_score": score,
        "resume_skills": resume_skills,
        "missing_skills": missing_skills
    })

# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)