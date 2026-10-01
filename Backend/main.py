from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from pypdf import PdfReader
from google import genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from dotenv import load_dotenv
import os
import io
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




model = SentenceTransformer("all-MiniLM-L6-v2")
def calculate_similarity(resume_text, job_description):
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    semantic_match_score = round(float(cosine_similarity(
    resume_embedding,
    job_embedding
)[0][0]) * 100, 2)

    return semantic_match_score


class ResumeData(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    skills: list[str] = []
    education: list[str] = []
    experience: list[str] = []
    projects: list[str] = []
    resume_text: str = ""

class AIAnalysisRequest(BaseModel):
    resume: ResumeData
    job_description: str   

class CareerRecommendationRequest(BaseModel):
    resume: ResumeData
    job_description: str    

class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: list[str]    

class CandidateRankingRequest(BaseModel):
    candidates: list[ResumeData]
    job: JobDescription    

load_dotenv()

gemini_client = genai.Client()

client = None

def generate_career_recommendations(resume_text, job_description):

    prompt = f"""
You are an expert AI career advisor and recruitment assistant.

Analyze the candidate's resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide the following:

1. Matching Skills
2. Missing Skills
3. Skills the candidate should learn
4. Suitable Job Roles
5. Interview Preparation Topics
6. Overall Career Recommendation

Give the response in a clear and easy-to-read format.
"""

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text



    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    # Skills to check
    skills = [
        "python",
        "sql",
        "fastapi",
        "flask",
        "django",
        "react",
        "javascript",
        "html",
        "css",
        "git",
        "github",
        "mysql",
        "postgresql",
        "mongodb",
        "rest api",
        "machine learning",
        "artificial intelligence",
        "power bi",
        "tableau",
        "excel",
        "docker",
        "aws",
        "azure"
    ]

    matched_skills = []
    missing_skills = []

    for skill in skills:
        if skill in job_lower:
            if skill in resume_lower:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    # Calculate skill match percentage
    total_required = len(matched_skills) + len(missing_skills)

    if total_required > 0:
        skill_match_percentage = round(
            (len(matched_skills) / total_required) * 100
        )
    else:
        skill_match_percentage = 0

    # Generate summary
    if skill_match_percentage >= 80:
        summary = "Your resume has a strong match with the job description."
    elif skill_match_percentage >= 60:
        summary = "Your resume has a good match with the job description, with some skills that can be improved."
    elif skill_match_percentage >= 40:
        summary = "Your resume has a moderate match with the job description and has several skill gaps."
    else:
        summary = "Your resume has a limited match with the job description and requires additional relevant skills."

    # Generate recommendations
    recommendations = []

    if missing_skills:
        recommendations.append(
            "Consider improving or gaining experience in: "
            + ", ".join(missing_skills)
        )

    if "python" in job_lower and "python" not in resume_lower:
        recommendations.append(
            "Strengthen your Python programming and problem-solving skills."
        )

    if "sql" in job_lower and "sql" not in resume_lower:
        recommendations.append(
            "Practice SQL queries, joins, subqueries, and database concepts."
        )

    if "rest api" in job_lower and "rest api" not in resume_lower:
        recommendations.append(
            "Build a REST API project using FastAPI or Flask."
        )

    if "git" in job_lower and "git" not in resume_lower:
        recommendations.append(
            "Learn Git and GitHub workflows such as branching, commits, and pull requests."
        )

    if not recommendations:
        recommendations.append(
            "Continue building projects that demonstrate the required skills."
        )

    return {
        "summary": summary,
        "skill_match_percentage": skill_match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }

def extract_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return ""

def extract_name(text):
    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if line:
            return line

    return ""
def extract_phone(text):
    pattern = r'\b[6-9]\d{9}\b'
    match = re.search(pattern, text)

    if match:
        return match.group()

    return ""
def extract_skills(text):
    skills_list = [
        "Python",
        "SQL",
        "React",
        "HTML",
        "CSS",
        "JavaScript",
        "Django",
        "Flask",
        "FastAPI",
        "MongoDB",
        "MySQL",
        "PostgreSQL",
        "Git",
        "GitHub",
        "Docker",
        "AWS",
        "Azure",
        "Google Cloud",
        "Power BI",
        "Tableau",
        "Excel",
        "Flutter",
        "Framer"
    ]

    found_skills = []

    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills

def clean_list(items):
    cleaned = []

    for item in items:
        item = item.strip()

        if item and item not in cleaned:
            cleaned.append(item)

    return cleaned

def extract_education(text):
    education = []

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if any(keyword in line.lower() for keyword in [
            "b.e", "b.tech", "m.e", "m.tech",
            "b.sc", "m.sc", "bca", "mca",
            "b.com", "m.com", "mba",
            "bachelor", "master",
            "university", "college"
        ]):
            education.append(line)

    return education

def extract_experience(text):
    experience = []

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if any(keyword in line.lower() for keyword in [
            "experience",
            "developer",
            "engineer",
            "intern",
            "analyst",
            "associate",
            "software",
            "worked",
            "working"
        ]):
            experience.append(line)

    return experience

def extract_projects(text):
    projects = []

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if any(keyword in line.lower() for keyword in [
            "project",
            "developed",
            "built",
            "created",
            "implemented",
            "application",
            "platform"
        ]):
            projects.append(line)

    return projects

def calculate_match_score(resume_skills, job_skills):
    resume_skills = {skill.lower().strip() for skill in resume_skills}
    job_skills = {skill.lower().strip() for skill in job_skills}

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    if len(job_skills) == 0:
        score = 0
    else:
        score = (len(matched_skills) / len(job_skills)) * 100

    return {
        "score": round(score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills)
    }



def calculate_experience_match(resume_experience, job_description):

    resume_experience_text = " ".join(resume_experience).lower()
    job_description_text = job_description.lower()

    experience_keywords = [
        "developer",
        "software",
        "backend",
        "frontend",
        "python",
        "api",
        "fastapi",
        "django",
        "flask",
        "database",
        "sql",
        "machine learning",
        "data",
        "cloud",
        "aws",
        "azure",
        "docker"
    ]

    matched_keywords = []

    for keyword in experience_keywords:
        if keyword in resume_experience_text and keyword in job_description_text:
            matched_keywords.append(keyword)

    if len(experience_keywords) == 0:
        score = 0
    else:
        score = (
            len(matched_keywords)
            / len([
                keyword
                for keyword in experience_keywords
                if keyword in job_description_text
            ])
            * 100
        ) if any(
            keyword in job_description_text
            for keyword in experience_keywords
        ) else 0

    return {
        "score": round(score, 2),
        "matched_keywords": matched_keywords
    }

def calculate_education_match(resume_education, job_description):

    resume_education_text = " ".join(resume_education).lower()
    job_description_text = job_description.lower()

    education_keywords = [
        "b.e",
        "b.tech",
        "m.e",
        "m.tech",
        "b.sc",
        "m.sc",
        "bca",
        "mca",
        "b.com",
        "m.com",
        "mba",
        "bachelor",
        "master",
        "computer science",
        "information technology",
        "engineering",
        "data science"
    ]

    matched_keywords = []

    for keyword in education_keywords:
        if keyword in resume_education_text and keyword in job_description_text:
            matched_keywords.append(keyword)

    required_keywords = [
        keyword
        for keyword in education_keywords
        if keyword in job_description_text
    ]

    if len(required_keywords) == 0:
        score = 0
    else:
        score = (
            len(matched_keywords)
            / len(required_keywords)
        ) * 100

    return {
        "score": round(score, 2),
        "matched_keywords": matched_keywords
    }

def calculate_project_match(resume_projects, job_description):

    resume_projects_text = " ".join(resume_projects).lower()
    job_description_text = job_description.lower()

    project_keywords = [
        "python",
        "sql",
        "fastapi",
        "django",
        "flask",
        "react",
        "javascript",
        "html",
        "css",
        "mongodb",
        "mysql",
        "postgresql",
        "api",
        "backend",
        "frontend",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "ai",
        "data science",
        "data analysis",
        "cloud",
        "aws",
        "azure",
        "docker",
        "application",
        "platform"
    ]

    matched_keywords = []

    for keyword in project_keywords:
        if keyword in resume_projects_text and keyword in job_description_text:
            matched_keywords.append(keyword)

    required_keywords = [
        keyword
        for keyword in project_keywords
        if keyword in job_description_text
    ]

    if len(required_keywords) == 0:
        score = 0
    else:
        score = (
            len(matched_keywords)
            / len(required_keywords)
        ) * 100

    return {
        "score": round(score, 2),
        "matched_keywords": matched_keywords
    }   


def get_candidate_recommendation(score):

    if score >= 90:
        return "Strong Candidate"
    elif score >= 75:
        return "Good Candidate"
    elif score >= 60:
        return "Moderate Candidate"
    else:
        return "Not Recommended"


def generate_candidate_explanation(
    matched_skills,
    missing_skills,
    matched_experience_keywords,
    matched_education_keywords,
    matched_project_keywords
):

    strengths = []
    gaps = []

    if matched_skills:
        strengths.append(
            "Strong skill match: " +
            ", ".join(matched_skills)
        )

    if matched_experience_keywords:
        strengths.append(
            "Relevant experience: " +
            ", ".join(matched_experience_keywords)
        )

    if matched_education_keywords:
        strengths.append(
            "Relevant education: " +
            ", ".join(matched_education_keywords)
        )

    if matched_project_keywords:
        strengths.append(
            "Relevant project experience: " +
            ", ".join(matched_project_keywords)
        )

    if missing_skills:
        gaps.append(
            "Missing required skills: " +
            ", ".join(missing_skills)
        )

    return {
        "strengths": strengths,
        "gaps": gaps
    }    


def calculate_candidate_match(resume: ResumeData, job: JobDescription):

    resume_text = " ".join([
        resume.name,
        resume.email,
        resume.phone,
        " ".join(resume.skills),
        " ".join(resume.education),
        " ".join(resume.experience),
        " ".join(resume.projects)
    ])

    job_text = " ".join([
        job.title,
        job.description,
        " ".join(job.required_skills)
    ])

    # Semantic matching
    semantic_score = calculate_similarity(
        resume_text,
        job_text
    )

    # Skill matching
    skill_result = calculate_match_score(
        resume.skills,
        job.required_skills
    )

    # Experience matching
    experience_result = calculate_experience_match(
        resume.experience,
        job.description
    )

    education_result = calculate_education_match(
    resume.education,
    job.description
)

    project_result = calculate_project_match(
    resume.projects,
    job.description
)

    # Overall score
    overall_match_score = round(
    (semantic_score * 0.3) +
    (skill_result["score"] * 0.3) +
    (experience_result["score"] * 0.2) +
    (education_result["score"] * 0.1) +
    (project_result["score"] * 0.1),
    2
)

    recommendation = get_candidate_recommendation(
    overall_match_score
)

    explanation = generate_candidate_explanation(
        skill_result["matched_skills"],
        skill_result["missing_skills"],
        experience_result["matched_keywords"],
        education_result["matched_keywords"],
        project_result["matched_keywords"]
)
    
    return {
        "job_title": job.title,
        "semantic_match_score": semantic_score,
        "skill_match_score": skill_result["score"],
        "experience_match_score": experience_result["score"],
        "education_match_score": education_result["score"],
        "project_match_score": project_result["score"],
        "overall_match_score": overall_match_score,
        "recommendation": recommendation,
        "strengths": explanation["strengths"],
        "gaps": explanation["gaps"],
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "matched_experience_keywords": experience_result["matched_keywords"],
        "matched_education_keywords": education_result["matched_keywords"],
        "matched_project_keywords": project_result["matched_keywords"]
    }


def rank_candidates(candidates):
    return sorted(
        candidates,
        key=lambda x: x["overall_match_score"],
        reverse=True
    )

def generate_ai_analysis(resume_text, job_description):

    prompt = f"""
You are an expert AI recruitment assistant.

Analyze the candidate's resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide the following:

1. Resume Summary
2. Matching Skills
3. Missing Skills
4. Experience Analysis
5. Education Relevance
6. Project Relevance
7. Strengths
8. Areas for Improvement
9. Interview Preparation
10. Overall Candidate Assessment

Give the response in a clear, professional and easy-to-read format.
"""

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

@app.post("/ai-analysis")
def ai_analysis(request: AIAnalysisRequest):
    analysis = generate_ai_analysis(
        request.resume.resume_text,
        request.job_description
    )

    return {
        "message": "AI analysis generated successfully",
        "analysis": analysis
    }


@app.post("/rank-candidates")
def rank_candidates_api(candidates: list[dict]):

    ranked_candidates = rank_candidates(candidates)

    for index, candidate in enumerate(ranked_candidates):
        candidate["rank"] = index + 1

    return {
        "ranked_candidates": ranked_candidates
    }
    

@app.get("/")
def home():
    return {
        "message": "AI Recruitment & Career Intelligence Platform API is running!"
    }


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    contents = await file.read()

    pdf_file = io.BytesIO(contents)

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    email = extract_email(text)
    name = extract_name(text)
    phone = extract_phone(text)
    skills = clean_list(extract_skills(text))
    education = clean_list(extract_education(text))
    experience = clean_list(extract_experience(text))
    projects = clean_list(extract_projects(text))

    resume_data = ResumeData(
       name=name,
       email=email,
       phone=phone,
       skills=skills,
       education=education,
       experience=experience,
       projects=projects,
       resume_text=text
)

    return {
    "filename": file.filename,
    "message": "Resume uploaded and text extracted successfully!",
    "resume_data": resume_data,
    "resume_text": text
}

@app.post("/job-description")
def create_job_description(job: JobDescription):
    return {
        "message": "Job description received successfully!",
        "job": job
    }

@app.post("/match-resume")
def match_resume(
    resume: ResumeData,
    job: JobDescription
):

    return calculate_candidate_match(
        resume,
        job
    )


@app.post("/rank-resumes")
def rank_resumes(request: CandidateRankingRequest):

    ranked_candidates = []

    for candidate in request.candidates:

        match_result = calculate_candidate_match(
            candidate,
            request.job
        )

        match_result["candidate_name"] = candidate.name

        ranked_candidates.append(match_result)

    ranked_candidates = rank_candidates(
        ranked_candidates
    )

    for index, candidate in enumerate(ranked_candidates):
        candidate["rank"] = index + 1

    return {
        "job_title": request.job.title,
        "total_candidates": len(ranked_candidates),
        "ranked_candidates": ranked_candidates
    }


@app.post("/career-recommendations")
def career_recommendations(request: CareerRecommendationRequest):
    recommendations = generate_career_recommendations(
        request.resume.resume_text,
        request.job_description
    )

    return {
        "message": "Career recommendations generated successfully",
        "recommendations": recommendations
    }


@app.get("/test-gemini")
def test_gemini():
    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say hello and confirm that Gemini is working."
    )

    return {
        "message": response.text
    }