import streamlit as st
import os
from parser import extract_text_from_pdf, extract_text_from_docx
from matcher import extract_skills, match_resume_with_jobs
from db_utils import init_db, add_job, get_jobs

init_db()
UPLOAD_FOLDER = os.path.join('resumes','uploaded')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title='Resume Analyzer + Job Matcher', layout='wide')
st.title("📄 Resume Analyzer + Job Matcher (Streamlit)")

menu = ["Upload Resume", "Post Job", "View Jobs"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Upload Resume":
    st.header("Upload Your Resume")
    uploaded_file = st.file_uploader("Upload PDF/DOCX/TXT", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text
        if uploaded_file.name.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif uploaded_file.name.lower().endswith(".docx"):
            text = extract_text_from_docx(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()

        resume_skills = set(extract_skills(text))
        st.subheader("Extracted Skills")
        if resume_skills:
            st.write(", ".join(sorted(resume_skills)))
        else:
            st.info("No skills detected with the current skill list / NER. Try a different resume or add more skills to the DB.")

        jobs = get_jobs()
        if jobs:
            matches = match_resume_with_jobs(resume_skills, jobs)
            st.subheader("Top Matching Jobs")
            for job in matches:
                st.markdown(f"**{job['title']}** at *{job['company']}* — **Match: {job['match_score']}%**\n\nRequired skills: {', '.join(job['skills'])}")
        else:
            st.warning("No jobs found in database. Please add some in 'Post Job'.")

elif choice == "Post Job":
    st.header("Post a Job")
    with st.form("job_form"):
        title = st.text_input("Job Title")
        company = st.text_input("Company")
        skills = st.text_area("Required Skills (comma-separated)")
        submitted = st.form_submit_button("Add Job")
        if submitted:
            skills_list = [s.strip() for s in skills.split(",") if s.strip()]
            add_job(title, company, skills_list)
            st.success(f"✅ Job '{title}' added successfully!")

elif choice == "View Jobs":
    st.header("Available Jobs")
    jobs = get_jobs()
    if jobs:
        for job in jobs:
            st.write(f"- **{job['title']}** at {job['company']} (Skills: {', '.join(job['skills'])})")
    else:
        st.warning("No jobs posted yet.")
