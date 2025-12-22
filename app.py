import streamlit as st
import pandas as pd
import docx
import PyPDF2
import re
from datetime import datetime

# ================= إعداد الصفحة =================
st.set_page_config(
    page_title="ATS | HR System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= CSS احترافي =================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #4b0f14 0%, #1a0003 65%);
    color: #f5f5f5;
    font-family: 'Segoe UI', sans-serif;
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background: url("https://i.imgur.com/8IuucQZ.png");
    opacity: 0.12;
    pointer-events: none;
}
.card {
    background: rgba(15, 0, 0, 0.75);
    border: 1px solid rgba(255, 90, 90, 0.25);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}
.result {
    font-size: 22px;
    font-weight: bold;
}
.junior { color:#ff7675; }
.mid { color:#fdcb6e; }
.senior { color:#00b894; }
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= العنوان =================
st.markdown("<h1>🧑‍💼 ATS – Applicant Tracking System</h1>", unsafe_allow_html=True)
st.markdown("نظام توظيف احترافي لإدارة وفرز المرشحين")

# ================= Session =================
if "candidates" not in st.session_state:
    st.session_state.candidates = []

# ================= رفع الملفات =================
uploaded_files = st.file_uploader(
    "📄 ارفع السير الذاتية",
    accept_multiple_files=True
)

# ================= أدوات القراءة =================
def extract_text(file):
    if file.name.lower().endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    elif file.name.lower().endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file.name.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
        return df.to_string()
    return ""

def extract_years(text):
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    return sorted(set(int(y) for y in years))

def calculate_experience(years):
    if len(years) < 2:
        return 0
    return min(datetime.now().year, max(years)) - min(years)

def classify(exp):
    if exp <= 2:
        return "Junior", "junior"
    elif exp <= 6:
        return
