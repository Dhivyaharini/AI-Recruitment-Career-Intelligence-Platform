import { useState } from 'react'
import axios from 'axios'
import './App.css'
import ReactMarkdown from 'react-markdown'

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const [file, setFile] = useState(null)
  const [resumeData, setResumeData] = useState(null)
  const [uploading, setUploading] = useState(false)

  const [jobTitle, setJobTitle] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [requiredSkills, setRequiredSkills] = useState('')
  const [jobMessage, setJobMessage] = useState('')

  const [matchResult, setMatchResult] = useState(null)
  const [matching, setMatching] = useState(false)

  const [aiAnalysis, setAiAnalysis] = useState(null)
  const [aiLoading, setAiLoading] = useState(false)

  const [careerRecommendations, setCareerRecommendations] = useState(null)
  const [careerLoading, setCareerLoading] = useState(false)

  // Test Backend Connection
  const testBackend = async () => {
    try {
      setLoading(true)

      const response = await axios.get('http://127.0.0.1:8000/')

      setMessage(response.data.message)
    } catch (error) {
      console.error(error)
      setMessage('Backend connection failed')
    } finally {
      setLoading(false)
    }
  }

  // Select Resume
  const handleFileChange = (event) => {
    setFile(event.target.files[0])
    setResumeData(null)
  }

  // Upload Resume
  const uploadResume = async () => {
    if (!file) {
      setMessage('Please select a resume PDF first.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    try {
      setUploading(true)
      setMessage('Uploading resume...')

      const response = await axios.post(
        'http://127.0.0.1:8000/upload-resume',
        formData
      )

      setMessage('Resume uploaded successfully!')
      setResumeData(response.data)

    } catch (error) {
      console.error(error)
      setMessage('Resume upload failed.')
    } finally {
      setUploading(false)
    }
  }


  const submitJobDescription = async () => {
  if (!jobTitle || !jobDescription || !requiredSkills) {
    setJobMessage('Please fill in all job details.')
    return
  }

  try {
    setJobMessage('Submitting job description...')

    const skillsArray = requiredSkills
      .split(',')
      .map((skill) => skill.trim())
      .filter((skill) => skill !== '')

    const response = await axios.post(
      'http://127.0.0.1:8000/job-description',
      {
        title: jobTitle,
        description: jobDescription,
        required_skills: skillsArray
      }
    )

    console.log(response.data)

    setJobMessage('Job description submitted successfully! ✅')

  } catch (error) {
    console.error(error)
    setJobMessage('Failed to submit job description.')
  }
}

    const matchResume = async () => {
  if (!resumeData) {
    setJobMessage('Please upload a resume first.')
    return
  }

  if (!jobTitle || !jobDescription || !requiredSkills) {
    setJobMessage('Please enter the complete job description.')
    return
  }

  try {
    setMatching(true)
    setMatchResult(null)
    setJobMessage('Analyzing resume against job...')

    const skillsArray = requiredSkills
      .split(',')
      .map((skill) => skill.trim())
      .filter((skill) => skill !== '')

    const response = await axios.post(
      'http://127.0.0.1:8000/match-resume',
      {
        resume: resumeData.resume_data,
        job: {
          title: jobTitle,
          description: jobDescription,
          required_skills: skillsArray
        }
      }
    )

    setMatchResult(response.data)
    setJobMessage('Resume analysis completed successfully! ✅')

  } catch (error) {
    console.error(error)
    setJobMessage('Failed to analyze resume.')
  } finally {
    setMatching(false)
  }
}

const generateAIAnalysis = async () => {
  if (!resumeData) {
    setJobMessage('Please upload a resume first.')
    return
  }

  if (!jobTitle || !jobDescription) {
    setJobMessage('Please enter the complete job description.')
    return
  }

  try {
    setAiLoading(true)
    setAiAnalysis(null)
    setJobMessage('Generating AI candidate analysis...')

    const response = await axios.post(
  'http://127.0.0.1:8000/ai-analysis',
  {
    resume: {
      ...resumeData.resume_data,
      resume_text: resumeData.resume_text
    },
    job_description: jobDescription
  }
)

    setAiAnalysis(response.data)
    setJobMessage('AI analysis generated successfully! 🤖')

  } catch (error) {
    console.error(error)
    setJobMessage('Failed to generate AI analysis.')
  } finally {
    setAiLoading(false)
  }
}

    const generateCareerRecommendations = async () => {
  if (!resumeData) {
    setJobMessage('Please upload a resume first.')
    return
  }

  if (!jobTitle || !jobDescription) {
    setJobMessage('Please enter the complete job description.')
    return
  }

  try {
    setCareerLoading(true)
    setCareerRecommendations(null)
    setJobMessage('Generating career recommendations...')

    const response = await axios.post(
      'http://127.0.0.1:8000/career-recommendations',
      {
        resume: {
          ...resumeData.resume_data,
          resume_text: resumeData.resume_text
        },
        job_description: jobDescription
      }
    )

    setCareerRecommendations(response.data)
    setJobMessage('Career recommendations generated successfully! 🎯')

  } catch (error) {
    console.error(error)
    setJobMessage('Failed to generate career recommendations.')
  } finally {
    setCareerLoading(false)
  }
}

  return (
    <div className="app">

      <h1>AI Recruitment & Career Intelligence Platform</h1>

      <p>
        Upload your resume and get AI-powered career insights.
      </p>

      {/* Backend Test */}
      <button onClick={testBackend}>
        {loading ? 'Connecting...' : 'Test Backend Connection'}
      </button>

      {message && (
        <div className="result">
          <h3>Message:</h3>
          <p>{message}</p>
        </div>
      )}

      <hr />

      <div className="resume-card">

  <h2>📄 Upload Your Resume</h2>

  <p className="section-description">
    Upload your resume in PDF format to analyze your skills and career opportunities.
  </p>

  <input
    type="file"
    accept=".pdf"
    onChange={handleFileChange}
  />

  <button onClick={uploadResume}>
    {uploading ? 'Uploading...' : 'Upload Resume'}
  </button>

</div>

      {/* Resume Result */}
      {resumeData && (
        <div className="result">

          <h3>Resume Details ✅</h3>

          <p>
            <strong>File:</strong> {resumeData.filename}
          </p>

          <p>
            <strong>Name:</strong>{' '}
            {resumeData.resume_data?.name || 'Not detected'}
          </p>

          <p>
            <strong>Email:</strong>{' '}
            {resumeData.resume_data?.email || 'Not detected'}
          </p>

          <p>
            <strong>Phone:</strong>{' '}
            {resumeData.resume_data?.phone || 'Not detected'}
          </p>

          <p>
            <strong>Skills:</strong>{' '}
            {resumeData.resume_data?.skills?.join(', ') || 'Not detected'}
          </p>

        </div>


      
      )}


      <hr />

<h2>Enter Job Description</h2>

<div className="job-form">

  <input
    type="text"
    placeholder="Job Title"
    value={jobTitle}
    onChange={(e) => setJobTitle(e.target.value)}
  />

  <br />
  <br />

  <textarea
    placeholder="Enter Job Description"
    value={jobDescription}
    onChange={(e) => setJobDescription(e.target.value)}
    rows="6"
  />

  <br />
  <br />

  <input
    type="text"
    placeholder="Required Skills (Python, SQL, FastAPI)"
    value={requiredSkills}
    onChange={(e) => setRequiredSkills(e.target.value)}
  />

  <br />
  <br />

  <button onClick={submitJobDescription}>
    Submit Job Description
  </button>

  <br />
<br />

<button onClick={matchResume}>
  {matching ? 'Analyzing...' : 'Analyze Candidate'}
</button>

<br />
<br />

<button onClick={generateAIAnalysis}>
  {aiLoading ? 'Generating AI Analysis...' : 'Generate AI Analysis 🤖'}
</button>

<button onClick={generateCareerRecommendations}>
  {careerLoading
    ? 'Generating Career Recommendations...'
    : 'Get Career Recommendations 🎯'}
</button>

  {jobMessage && (
    <div className="result">
      <p>{jobMessage}</p>
    </div>
  )}

</div>

```jsx
{matchResult && (
  <div className="match-dashboard">

    <h2>🎯 Candidate Match Result</h2>

    <div className="overall-score">
      <h3>Overall Match</h3>
      <div className="score-circle">
        {matchResult.overall_match_score}%
      </div>
      <p>{matchResult.recommendation}</p>
    </div>

    <h3>📊 Match Breakdown</h3>

    <div className="score-grid">

      <div className="score-card">
        <h4>Semantic Match</h4>
        <strong>{matchResult.semantic_match_score}%</strong>
      </div>

      <div className="score-card">
        <h4>Skill Match</h4>
        <strong>{matchResult.skill_match_score}%</strong>
      </div>

      <div className="score-card">
        <h4>Experience Match</h4>
        <strong>{matchResult.experience_match_score}%</strong>
      </div>

      <div className="score-card">
        <h4>Education Match</h4>
        <strong>{matchResult.education_match_score}%</strong>
      </div>

      <div className="score-card">
        <h4>Project Match</h4>
        <strong>{matchResult.project_match_score}%</strong>
      </div>

    </div>

    <div className="skills-section">

      <div className="skill-box">
        <h3>🟢 Matched Skills</h3>

        {matchResult.matched_skills?.length > 0 ? (
          matchResult.matched_skills.map((skill, index) => (
            <span className="skill-tag matched" key={index}>
              {skill}
            </span>
          ))
        ) : (
          <p>No matched skills</p>
        )}
      </div>

      <div className="skill-box">
        <h3>🔴 Missing Skills</h3>

        {matchResult.missing_skills?.length > 0 ? (
          matchResult.missing_skills.map((skill, index) => (
            <span className="skill-tag missing" key={index}>
              {skill}
            </span>
          ))
        ) : (
          <p>No missing skills 🎉</p>
        )}
      </div>

    </div>

    <div className="insights">

      <div>
        <h3>💪 Strengths</h3>

        {matchResult.strengths?.map((strength, index) => (
          <p key={index}>✓ {strength}</p>
        ))}
      </div>

      <div>
        <h3>⚠️ Skill Gaps</h3>

        {matchResult.gaps?.map((gap, index) => (
          <p key={index}>• {gap}</p>
        ))}
      </div>

    </div>

  </div>
)}
```

{careerRecommendations && (
  <div className="result">
    <h2>🎯 Career Recommendations</h2>

    <div className="career-recommendations">
      <pre>{careerRecommendations.recommendations}</pre>
    </div>
  </div>
)}


{aiAnalysis && (
  <div className="ai-analysis-card">
    <h2>🤖 AI Candidate Analysis</h2>

    <p className="ai-description">
      AI-powered evaluation of the candidate based on
      the resume and job description.
    </p>

    <div className="ai-analysis-content">
  <div className="ai-result">
    <ReactMarkdown>
      {typeof aiAnalysis === 'string'
        ? aiAnalysis
        : aiAnalysis.analysis || 'No analysis available.'}
    </ReactMarkdown>
  </div>
</div>

  </div>
)}


    </div>

        
  )
}

export default App