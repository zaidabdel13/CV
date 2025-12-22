import streamlit as st
import pandas as pd
import docx
import PyPDF2
import re
from dateutil import parser

st.set_page_config(page_title="🤖 روبوت قراءة الخبرة مثل الإنسان", layout="wide")
st.title("🤖 روبوت قراءة الخبرة من السير الذاتية")
st.write("ارفع ملفات PDF, DOCX أو Excel وسيقوم Streamlit بحساب سنوات الخبرة من التواريخ كما لو كان إنساناً يقرأها.")

uploaded_files = st.file_uploader("ارفع الملفات هنا", accept_multiple_files=True)

# دالة لاستخراج النصوص من الملفات
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
        df = pd.read_excel(file)
        return df.to_string()
    else:
        return ""

# دالة لحساب سنوات الخبرة من أي تواريخ في النص
def extract_experience_dates(text):
    # استخراج كل السنوات في النص (4 أرقام)
    potential_dates = re.findall(r'\b(19|20)\d{2}\b', text)
    potential_dates = [int(d) for d in potential_dates]

    if not potential_dates:
        return "غير محدد"

    # فرز السنوات وتصحيح الفترات
    potential_dates.sort()
    total_years = 0
    for i in range(0, len(potential_dates)-1, 2):
        start = potential_dates[i]
        end = potential_dates[i+1]
        if end >= start:
            total_years += end - start

    # إذا لم توجد أزواج، نقدر نعطي تقدير من أول سنة حتى آخر سنة
    if total_years == 0 and len(potential_dates) >= 2:
        total_years = potential_dates[-1] - potential_dates[0]

    return total_years

# معالجة الملفات واظهار النتائج
if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 الملف: {file.name}")
        text = extract_text(file)
        if text:
            experience = extract_experience_dates(text)
            st.write(f"📝 سنوات الخبرة: {experience}")
        else:
            st.write("⚠️ لم يتمكن Streamlit من قراءة الملف.")
