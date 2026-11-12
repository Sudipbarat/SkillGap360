# SkillGap360 – AI Skill Passport

**Your AI-powered Skill Passport**

Discover, document and validate the skills already demonstrated in your professional experience.

**Live Application:** https://skillgap360-ai.streamlit.app/  
**GitHub Repository:** https://github.com/Sudipbarat/SkillGap360

---

## 1. Project Overview

SkillGap360 is an AI-powered Skill Passport application designed to help individuals identify, document and organise skills demonstrated through their professional experience and educational background.

Users can upload their CVs, extract relevant information using AI, review the identified skills, make corrections and download their skill profiles.

The application aims to make professional skills more visible, structured and easier to communicate.

## 2. Problem Statement

Traditional CVs often present professional experience in lengthy, unstructured formats. Identifying and documenting skills from these documents can be time-consuming.

Individuals may also struggle to identify the skills they have demonstrated through their education and work experience.

SkillGap360 addresses this problem by transforming CV information into a structured and reviewable Skill Passport.

## 3. Key Features

- **CV Upload:** Upload a CV for AI-powered information extraction.
- **AI Skill Extraction:** Identify skills demonstrated in the uploaded CV.
- **Evidence-Based Extraction:** Associate extracted skills with supporting information from the CV.
- **Profile Extraction:** Identify candidate details, education and professional experience.
- **Skill Review:** Review, edit and remove extracted skills before saving.
- **Skill Dashboard:** View a summary and visualisation of the extracted skills.
- **Data Export:** Download the reviewed Skill Passport as a CSV file.
- **Visual Insights:** Generate skill distribution charts and download visual reports.

## 4. How It Works

1. Upload a CV.
2. The application extracts relevant information from the document.
3. AI identifies skills and supporting evidence.
4. Review the extracted skills and profile information.
5. Edit or remove skills where necessary.
6. View the Skill Passport dashboard.
7. Download the structured skill information.

## 5. Technology Stack

| Component | Technology |
|---|---|
| Frontend and application framework | Streamlit |
| Programming language | Python |
| AI integration | Google Gemini API |
| PDF processing | PyPDF |
| Word document processing | python-docx |
| Data processing | Pandas |
| Data visualisation | Matplotlib |
| Deployment | Streamlit Community Cloud |
| Version control | GitHub |

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Google Gemini API key

### Clone the repository

```bash
git clone https://github.com/Sudipbarat/SkillGap360.git
cd SkillGap360
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the API key

Create a `.streamlit/secrets.toml` file and add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Never commit your API key or secrets file to GitHub.

### Run the application

```bash
python -m streamlit run app.py
```

## 7. AI Usage and Human Validation

Google Gemini API is used to extract structured information and identify skills from uploaded CVs.

AI-generated results are intended to assist users, not replace their judgement. Users can review, edit and remove extracted skills before finalising their Skill Passport.

The application does not intend to independently certify professional competence or make employment decisions.

## 8. Scope and Limitations

This version represents the Minimum Viable Product (MVP).

The current scope includes:

- CV-based skill extraction.
- Candidate profile and experience extraction.
- Manual review and editing of extracted skills.
- Skill visualisation and CSV export.

The current MVP does not include:

- User authentication and permanent database storage.
- HR or manager dashboards.
- Automated job-role matching.
- Skill-gap scoring.
- Personalised learning recommendations.
- Integration with external HR platforms.

## 9. Privacy and Security

- API credentials are stored using Streamlit secrets.
- Secret configuration files are excluded from Git version control.
- Uploaded CVs may be processed by the Google Gemini API.
- Users should avoid uploading sensitive personal information without understanding the applicable data-processing terms.
- The MVP does not provide permanent user account storage.

## 10. Future Scope

Potential future enhancements include:

- Personalised skill-gap analysis.
- Job-role and competency matching.
- AI-powered learning recommendations.
- User accounts and persistent Skill Passports.
- HR and organisational dashboards.
- Integration with recruitment and learning platforms.

## 11. Project Information

**Project Name:** SkillGap360 – AI Skill Passport  
**Programme:** Executive MBA, 2025–2027  
**Institution:** Indian Institute of Management Visakhapatnam  
**Project Type:** Digital Product Management – MVP

---

*SkillGap360 helps individuals discover, document and communicate the skills they already demonstrate.*
