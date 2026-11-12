
import streamlit as st
import pandas as pd
import json
import re
from io import BytesIO

from pypdf import PdfReader
from docx import Document
from google import genai

import io
import matplotlib.pyplot as plt
from collections import Counter

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="SkillGap360",
    page_icon="🎯",
    layout="wide"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
.main {
    background-color: #f7f8fc;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #18264a;
}
.stButton button {
    background-color: #5546e8;
    color: white;
    border-radius: 8px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.title("🎯 SkillGap360")
st.subheader("Your AI-powered Skill Passport")
st.write(
    "Discover, document and validate the skills "
    "already demonstrated in your professional experience."
)

st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.title("SkillGap360")
st.sidebar.caption("AI Skill Passport – MVP")

api_key = st.secrets["GEMINI_API_KEY"]

st.sidebar.info(
    "Your skills are extracted from your CV "
    "and must be reviewed by you."
)

# ---------------- FILE EXTRACTION ----------------

def extract_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif file_name.endswith(".docx"):
        document = Document(uploaded_file)
        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    elif file_name.endswith(".txt"):
        return uploaded_file.getvalue().decode(
            "utf-8", errors="ignore"
        )

    return ""


# ---------------- AI SKILL EXTRACTION ----------------

def analyse_cv(cv_text, api_key):

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a careful professional skills analyst.

Analyse the CV text below and identify skills that are
explicitly supported by the candidate's experience.

Rules:
1. Do not invent skills.
2. Do not assume proficiency levels.
3. Every skill must have supporting evidence copied
   or accurately referenced from the CV.
4. If evidence is unclear, do not include the skill.
5. Return valid JSON only.

Required JSON format:
{{
      "profile": {{
        "name": "Candidate name",
        "professional_title": "Professional title",
        "education": [
            {{
                "degree": "Degree",
                "institution": "Institution",
                "year": "Year"
            }}
        ],
        "experience": [
            {{
                "job_title": "Job title",
                "company": "Company",
                "duration": "Duration"
            }}
        ]
    }},
    "skills": [
    {{
      "skill": "Skill name",
      "evidence": "Supporting CV evidence",
      "category": "Technical / Business / Communication / Other"
    }}
  ]
}}

CV TEXT:
{cv_text[:25000]}
"""

    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
    
    )

    result = response.text.strip()
    result = re.sub(r"```json\s*", "", result)
    result = re.sub(r"\s*```$", "", result)

    return json.loads(result)


# ---------------- MAIN APPLICATION ----------------

st.header("1. Upload your CV")

uploaded_file = st.file_uploader(
    "Choose your CV",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX and TXT"
)

if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Extract My Skills", type="primary"):

        if not api_key:
            st.error(
                "Please enter your Gemini API key "
                "in the left sidebar."
            )

        else:
            try:
                with st.spinner(
                    "AI is analysing your CV..."
                ):
                    cv_text = extract_text(uploaded_file)

                    if not cv_text.strip():
                        st.error(
                            "No readable text found. "
                            "Please upload a text-based CV."
                        )
                    else:
                        result = analyse_cv(
                            cv_text, api_key
                        )

                        st.session_state["skills"] = (
                            result.get("skills", [])
                        )
                        st.session_state["profile"] = result.get("profile", {})
                        st.session_state["cv_name"] = (
                            uploaded_file.name
                        )

                        st.success(
                            "Skill extraction completed!"
                        )

            except Exception as error:
                st.error(
                    f"Something went wrong: {error}"
                )


# ---------------- SKILL PASSPORT ----------------

if "skills" in st.session_state:

    st.header("Candidate Dashboard")

    profile = st.session_state.get("profile", {})
    skills = st.session_state.get("skills", [])

    st.subheader(profile.get("name", "Candidate"))
    st.write(profile.get("professional_title", "Professional Profile"))

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Skills", len(skills))

    with col2:
        st.metric("Education Records", len(profile.get("education", [])))

    st.subheader("Education")
    for item in profile.get("education", []):
        st.write(
            f"🎓 {item.get('degree', '')} | "
            f"{item.get('institution', '')} | "
            f"{item.get('year', '')}"
        )

    st.subheader("Work Experience")
    for item in profile.get("experience", []):
        st.write(
            f"💼 {item.get('job_title', '')} | "
            f"{item.get('company', '')} | "
            f"{item.get('duration', '')}"
        )

    if skills:
        categories = pd.Series(
            [item.get("category", "Other") for item in skills]
        ).value_counts()

        chart1, chart2 = st.columns(2)

        with chart1:
            st.subheader("Skills Distribution")
            fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#1e1e1e")
        ax.set_facecolor("#1e1e1e")
        categories.plot.pie(autopct="%1.1f%%", ax=ax, textprops={"color": "white"})
        ax.set_ylabel("")
        st.pyplot(fig)
        plt.close(fig)

        with chart2:
            st.subheader("Skills by Category")
            st.bar_chart(categories)
    st.divider()

    st.header("2. Review Your Skill Passport")

    st.write(
        "Please review the extracted skills and "
        "correct anything that is inaccurate."
    )

    skills = st.session_state["skills"]

    if skills:

        df = pd.DataFrame(skills)

        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            width="stretch",
            column_config={
                "skill": st.column_config.TextColumn(
                    "Skill",
                    required=True
                ),
                "evidence": st.column_config.TextColumn(
                    "Supporting CV Evidence",
                    width="large",
                    required=True
                ),
                "category": st.column_config.SelectboxColumn(
                    "Category",
                    options=[
                        "Technical",
                        "Business",
                        "Communication",
                        "Other"
                    ]
                )
            }
        )

        if st.button("Save My Reviewed Skills"):

            st.session_state["reviewed_skills"] = (
                edited_df.to_dict("records")
            )

            st.success(
                "Your reviewed skills have been saved "
                "for this session."
            )

    else:
        st.info(
            "No supported skills were identified. "
            "Try another CV."
        )


# ---------------- FINAL PASSPORT ----------------

if "reviewed_skills" in st.session_state:

    st.divider()

    st.header("3. Your Skill Passport")

    final_skills = st.session_state["reviewed_skills"]

    st.metric(
        "Reviewed Skills",
        len(final_skills)
    )

    st.dataframe(
        pd.DataFrame(final_skills),
        use_container_width=True,
        hide_index=True
    )

    passport = pd.DataFrame(final_skills)

    st.subheader("Your Skill Insights")

    category_counts = passport["category"].fillna("Uncategorized").value_counts()

    fig, ax = plt.subplots(figsize=(8, 4))
    category_counts.plot(kind="bar", ax=ax)

    ax.set_title("Your Skills by Category")
    ax.set_xlabel("Skill Category")
    ax.set_ylabel("Number of Skills")
    plt.xticks(rotation=0)
    fig.tight_layout()

    st.pyplot(fig)

    image_buffer = io.BytesIO()
    fig.savefig(image_buffer, format="png", dpi=200, bbox_inches="tight")
    image_buffer.seek(0)

    st.download_button(
        "Download Skill Insights (PNG)",
        data=image_buffer.getvalue(),
        file_name="SkillGap360_Insights.png",
        mime="image/png"
    )

    plt.close(fig)
    st.download_button(
        "Download My Skill Passport (CSV)",
        data=passport.to_csv(index=False),
        file_name="SkillGap360_Skill_Passport.csv",
        mime="text/csv"
    )

    st.caption(
        "This passport is based on CV evidence reviewed "
        "and approved by the employee. It is not an "
        "automated employment assessment."
    )

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "SkillGap360 | AI-assisted skill discovery | "
    "Employee-controlled skill verification"
)
