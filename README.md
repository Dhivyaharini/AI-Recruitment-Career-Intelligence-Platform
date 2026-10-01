\# 🤖 AI Recruitment \& Career Intelligence Platform



An AI-powered full-stack platform designed to assist recruiters and job seekers with resume analysis, job matching, candidate evaluation, and career recommendations.



The platform analyzes a candidate's resume against a job description and provides meaningful insights using semantic matching and Generative AI.



\---



\## 🚀 Project Overview



The \*\*AI Recruitment \& Career Intelligence Platform\*\* helps simplify the recruitment process by combining traditional resume analysis with AI-powered insights.



A recruiter can upload a candidate's resume and provide a job description. The system analyzes the candidate's skills, experience, education, and projects, then generates a job-match score and AI-based recommendations.



The platform also provides career guidance such as missing skills, suitable roles, learning recommendations, and interview preparation topics.



\---



\## ✨ Key Features



\### 📄 Resume Upload \& Parsing

\- Upload candidate resumes in PDF format

\- Extract resume text automatically

\- Identify candidate information such as:

&#x20; - Name

&#x20; - Email

&#x20; - Phone

&#x20; - Skills

&#x20; - Education

&#x20; - Experience

&#x20; - Projects



\### 🎯 Resume–Job Matching

\- Compare resumes with job descriptions

\- Calculate a candidate match score

\- Use semantic similarity for better matching

\- Analyze:

&#x20; - Skills

&#x20; - Experience

&#x20; - Education

&#x20; - Projects



\### 🧠 AI-Powered Candidate Analysis

Generative AI provides:

\- Candidate strengths

\- Missing skills

\- Experience relevance

\- Overall candidate analysis

\- Recruitment-oriented recommendations



\### 💼 Career Intelligence

The platform can provide:

\- Suitable job roles

\- Skills to learn

\- Missing skill recommendations

\- Interview preparation topics

\- Career recommendations



\### 📊 Candidate Evaluation

Candidates can be evaluated and ranked based on their relevance to a given job description.



\---



\## 🛠️ Tech Stack



\### Frontend

\- React.js

\- JavaScript

\- HTML5

\- CSS3

\- Axios

\- React Markdown

\- Vite



\### Backend

\- Python

\- FastAPI

\- REST APIs

\- Uvicorn



\### AI / Machine Learning

\- Sentence Transformers

\- Semantic Embeddings

\- Cosine Similarity

\- Generative AI



\### Resume Processing

\- PyPDF



\### Development Tools

\- Git

\- GitHub

\- VS Code



\---



\## 🏗️ Project Architecture



```text

AI-Recruitment-Career-Intelligence-Platform

│

├── Backend

│   └── main.py

│

├── Frontend

│   ├── src

│   │   ├── App.jsx

│   │   ├── App.css

│   │   ├── api.js

│   │   ├── index.css

│   │   └── main.jsx

│   │

│   ├── public

│   ├── package.json

│   └── vite.config.js

│

├── .gitignore

└── README.md



















Candidate Resume

&#x20;      │

&#x20;      ▼

&#x20;  PDF Upload

&#x20;      │

&#x20;      ▼

&#x20;Resume Text Extraction

&#x20;      │

&#x20;      ▼

&#x20;Resume Data Analysis

&#x20;      │

&#x20;      ├───────────────┐

&#x20;      ▼               ▼

Job Description    Candidate Data

&#x20;      │               │

&#x20;      └───────┬───────┘

&#x20;              ▼

&#x20;     Semantic Matching

&#x20;              │

&#x20;              ▼

&#x20;       Match Score

&#x20;              │

&#x20;              ▼

&#x20;      AI Candidate Analysis

&#x20;              │

&#x20;              ▼

&#x20;  Career \& Interview Insights





\*\*\*\*Matching Approach\*\*\*\*



The platform combines multiple factors to evaluate candidate-job compatibility.



The matching logic considers:



Semantic similarity

Skill matching

Experience relevance

Education

Project relevance



Semantic matching is performed using sentence embeddings and cosine similarity, allowing the system to identify similarities in meaning rather than relying only on exact keyword matches.





🔌 Backend API



The backend is developed using FastAPI and exposes REST API endpoints for communication between the React frontend and Python backend.



Example operations include:



POST /upload-resume

POST /match-resume

POST /job-description

POST /rank-resumes

POST /ai-analysis



FastAPI also provides interactive API documentation through:



http://127.0.0.1:8000/docs



💻 Running the Project Locally

1\. Clone the repository

git clone https://github.com/Dhivyaharini/AI-Recruitment-Career-Intelligence-Platform.git



cd AI-Recruitment-Career-Intelligence-Platform



2\. Backend Setup



Navigate to the backend:



cd Backend



Create a virtual environment:



python -m venv venv



Activate the virtual environment on Windows:



venv\\Scripts\\activate



Install the required Python packages:



pip install -r requirements.txt



Create a .env file and add your AI API key:



GEMINI\_API\_KEY=your\_api\_key\_here



Then start the FastAPI server:



uvicorn main:app --reload



Backend:



http://127.0.0.1:8000



API documentation:



http://127.0.0.1:8000/docs



3\. Frontend Setup



Open another terminal and navigate to:



cd Frontend



Install dependencies:



npm install



Start the React development server:



npm run dev



The frontend will normally be available at:



http://localhost:5173



🔐 Environment Variables



API keys and other sensitive credentials should be stored in .env files.



Example:



GEMINI\_API\_KEY=your\_api\_key\_here



The .env file is excluded from Git using .gitignore.



Never commit API keys or other secrets to GitHub.



🎯 Use Cases

For Recruiters

Analyze candidate resumes

Compare candidates against job descriptions

Identify skill gaps

Evaluate candidate-job compatibility

Rank candidates



For Job Seekers



Understand resume-job compatibility

Identify missing skills

Discover suitable roles

Prepare for interviews

Get career learning recommendations





🌱 Future Enhancements

User authentication and role-based access

Recruiter dashboard

Candidate database

Multiple resume comparison dashboard

Job recommendation engine

Resume improvement suggestions

Interview question generation

Application tracking

Cloud deployment

Advanced analytics dashboard











