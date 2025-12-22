import streamlit as st
import pandas as pd
import docx
import PyPDF2
import re
from datetime import datetime

st.set_page_config(page_title="🤖 محلل خبرة عملي", layout="wide")
st.title("🤖 محلل سنوات الخبرة من السير الذاتية")
st.write("تحليل واقعي للتواريخ بدون AI – نتيجة منطقية مثل قراءة الإنسان")

uploaded_files = st.file_uploader("ارفع السيرة الذاتية", accept_multiple_files=True)

# ---------- قراءة النص ----------
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

# ---------- استخراج السنوات ----------
def extract_years(text):
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    years = sorted(set(int(y) for y in years))
    return years

# ---------- حساب الخبرة ----------
def calculate_experience(years):
    if len(years) < 2:
        return "غير واضح"

    start = min(years)
    end = max(years)

    current_year = datetime.now().year
    if end > current_year:
        end = current_year

    experience = end - start

    # منطق بشري: ما فيه خبرة 30 سنة لو الشخص عمره 25
    if experience < 0 or experience > 50:
        return "غير منطقي"

    return experience

# ---------- التنفيذ ----------
if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 {file.name}")
        text = extract_text(file)

        years = extract_years(text)

        if years:
            experience = calculate_experience(years)
            st.success(f"🧠 سنوات الخبرة التقديرية: {experience} سنة")

            with st.expander("🔍 تفاصيل التحليل"):
                st.write("السنوات المكتشفة:", years)
        else:
            st.error("❌ لم يتم العثور على تواريخ واضحة في السيرة")
