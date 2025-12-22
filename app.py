import streamlit as st
import pandas as pd
import docx
import PyPDF2
import re
from datetime import datetime

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="HR Resume Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== CSS احترافي ==================
st.markdown("""
<style>
/* خلفية الصفحة */
.stApp {
    background: radial-gradient(circle at top, #4b0f14 0%, #1a0003 60%);
    color: #f5f5f5;
    font-family: 'Segoe UI', sans-serif;
}

/* تأثير دخان */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background: url("https://i.imgur.com/8IuucQZ.png");
    opacity: 0.12;
    pointer-events: none;
    z-index: 0;
}

/* العنوان */
h1, h2, h3 {
    color: #ffdddd;
    letter-spacing: 1px;
}

/* كروت المرشحين */
.card {
    background: rgba(20, 0, 0, 0.75);
    border: 1px solid rgba(255, 80, 80, 0.25);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 30px rgba(0,0,0,0.6);
}

/* نتيجة الخبرة */
.result {
    font-size: 28px;
    font-weight: bold;
    color: #ff6b6b;
}

/* زر الرفع */
.stFileUploader label {
    color: #ffcccc !important;
    font-size: 18px;
}

/* إخفاء شعار Streamlit */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================== العنوان ==================
st.markdown("<h1>🧑‍💼 HR Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p>واجهة احترافية لتحليل السير الذاتية واستخراج سنوات الخبرة</p>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "📄 ارفع السير الذاتية (PDF / Word / Excel)",
    accept_multiple_files=True
)

# ================== قراءة النص ==================
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

# ================== تحليل الخبرة ==================
def extract_years(text):
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    years = sorted(set(int(y) for y in years))
    return years

def calculate_experience(years):
    if len(years) < 2:
        return "غير واضح"

    start = min(years)
    end = max(years)

    current_year = datetime.now().year
    if end > current_year:
        end = current_year

    exp = end - start
    if exp < 0 or exp > 50:
        return "غير منطقي"

    return f"{exp} سنة"

# ================== العرض ==================
if uploaded_files:
    for file in uploaded_files:
        text = extract_text(file)
        years = extract_years(text)
        experience = calculate_experience(years)

        st.markdown(f"""
        <div class="card">
            <h3>📄 {file.name}</h3>
            <p class="result">🧠 سنوات الخبرة: {experience}</p>
        </div>
        """, unsafe_allow_html=True)
