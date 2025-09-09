import sqlite3, os

DB_DIR = 'database'
DB_PATH = os.path.join(DB_DIR, 'jobs.db')

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  company TEXT,
                  skills TEXT)''')
    conn.commit()
    conn.close()

def add_job(title, company, skills):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO jobs (title, company, skills) VALUES (?, ?, ?)", (title, company, ",".join(skills)))
    conn.commit()
    conn.close()

def get_jobs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, company, skills FROM jobs")
    rows = c.fetchall()
    conn.close()
    jobs = []
    for r in rows:
        skills = r[3] or ''
        skills_list = [s.strip() for s in skills.split(',')] if skills else []
        jobs.append({'id': r[0], 'title': r[1], 'company': r[2], 'skills': skills_list})
    return jobs
