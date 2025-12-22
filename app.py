import streamlit as st
import pandas as pd
import docx
import PyPDF2
import re

st.set_page_config(page_title="🤖 روبوت قراءة السير الذاتية بدون AI", layout="wide")
st.title("🤖 روبوت قراءة السير الذاتية")
st.write("ارفع ملفات PDF, DOCX أو Excel وسيقوم Streamlit باستخراج عدد سنوات الخبرة مباشرة.")

uploaded_files = st.file_uploader("ارفع الملفات هنا", accept_multiple_files=True)

# دالة لاستخراج النص من الملفات
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

# دالة لاستخراج عدد سنوات الخبرة من النص باستخدام Regex
def extract_experience(text):
    # يبحث عن نماذج عربية
    arabic_matches = re.findall(r'(\d+)\s*(?:سنوات\s*خبرة|سنة\s*خبرة)', text)
    # يبحث عن نماذج انجليزية
    english_matches = re.findall(r'(\d+)\s*(?:years\s*experience|year\s*experience)', text, re.IGNORECASE)
    all_matches = arabic_matches + english_matches
    if all_matches:
        return max(map(int, all_matches))  # يعطينا أعلى عدد سنوات مذكور
    else:
        return "غير محدد"

# معالجة الملفات
if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 الملف: {file.name}")
        text = extract_text(file)
        if text:
            experience = extract_experience(text)
            st.write(f"📝 سنوات الخبرة: {experience}")
        else:
            st.write("⚠️ لم يتمكن Streamlit من قراءة الملف.")
