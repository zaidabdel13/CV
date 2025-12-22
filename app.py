import streamlit as st
import openai
import pandas as pd
import docx
import PyPDF2

# -----------------------------
# قراءة مفتاح OpenAI من Streamlit Secrets
# -----------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# إعداد واجهة التطبيق
st.set_page_config(page_title="🤖 روبوت قراءة السير الذاتية", layout="wide")
st.title("🤖 روبوت قراءة السير الذاتية")
st.write("ارفع ملفات PDF, DOCX أو Excel وسيقوم الروبوت بتحليلها واستخراج عدد سنوات الخبرة.")

# رفع ملفات متعددة
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

# دالة لطلب OpenAI واستخراج عدد سنوات الخبرة
def get_experience(text):
    prompt = f"اقرأ النص التالي واخبرني بعدد سنوات الخبرة المذكورة:\n{text}\nجاوب فقط بعدد سنوات الخبرة بشكل واضح."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"خطأ في قراءة الخبرة: {e}"

# معالجة الملفات واظهار النتائج
if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 الملف: {file.name}")
        text = extract_text(file)
        if text:
            experience = get_experience(text)
            st.write(f"📝 سنوات الخبرة: {experience}")
        else:
            st.write("⚠️ لم يتمكن الروبوت من قراءة الملف.")
