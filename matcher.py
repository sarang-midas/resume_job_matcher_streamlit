import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# load spaCy - if not available, callers should handle exception
try:
    nlp = spacy.load('en_core_web_sm')
except Exception:
    nlp = None

# a small built-in skill bank for fallback simple matching
SKILL_BANK = ['python','flask','django','sql','machine learning','data analysis','javascript','react','html','css','tensorflow','pytorch']

def extract_skills(text):
    text_l = text.lower() if text else ''
    skills = set()
    # use spaCy NER if available (but default model won't label 'SKILL' without custom training)
    if nlp:
        doc = nlp(text_l)
        # try to extract nouns/phrases that could be skills
        for chunk in doc.noun_chunks:
            token = chunk.text.strip()
            if token in SKILL_BANK:
                skills.add(token)
    # fallback: keyword matching
    for s in SKILL_BANK:
        if s in text_l:
            skills.add(s)
    return skills

def match_resume_with_jobs(resume_skills, jobs):
    resume_skills_set = set([s.lower() for s in resume_skills]) if resume_skills else set()
    matches = []
    for job in jobs:
        job_skills = set([s.lower() for s in job.get('skills', [])])
        overlap = len(resume_skills_set & job_skills)
        score = round((overlap / len(job_skills) * 100), 2) if job_skills else 0.0
        matches.append({**job, 'match_score': score})
    return sorted(matches, key=lambda x: x['match_score'], reverse=True)
