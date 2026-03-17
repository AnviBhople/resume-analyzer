 Resume Analyzer – AI-Powered Job Match Tool

An intelligent full-stack web application that analyzes a resume against a job description and provides a match score, skill insights and improvement suggestions.

This project combines **Flask (backend)** and **React (frontend)** with machine learning techniques to deliver meaningful resume evaluation.



Features

-  Upload resume in PDF format
-  Paste any job description
-  AI-based similarity scoring (TF-IDF + Cosine Similarity)
-  Automatic skill extraction
-  Detection of missing skills
-  Interactive skill match chart
-  Animated match score counter
-  Dark mode support
-  Modern responsive UI
-  Fully mobile-friendly design
-  Drag & drop file upload



 Tech Stack

 Frontend:
- React.js
- CSS (Modern UI Design)
- Recharts (Data Visualization)

 Backend:
- Flask
- Flask-CORS
- Scikit-learn
- PyMuPDF (PDF text extraction)

 How It Works

1. The user uploads a resume (PDF).
2. The system extracts text using PyMuPDF.
3. The resume text and job description are cleaned and processed.
4. TF-IDF vectorization converts text into numerical format.
5. Cosine similarity calculates the match percentage.
6. Skills are extracted and compared.
7. Results are displayed with visual insights.



 Installation & Setup

 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/resume-analyzer.git
cd resume-analyzer
