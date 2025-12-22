import streamlit as st
import openai
import pandas as pd
import docx
import PyPDF2

# -----------------------------
# مفتاح OpenAI المباشر للتشغيل التجريبي
# -----------------------------
openai.api_key = "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"

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

# دالة لطلب OpenAI واستخراج عدد سنوات الخبرة (متوافق مع openai>=1.0.0)
def get_experience(text):
    prompt = f"اقرأ النص التالي واخبرني بعدد سنوات الخبرة المذكورة:\n{text}\nجاوب فقط بعدد سنوات الخبرة بشكل واضح."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد يقوم باستخراج عدد سنوات الخبرة من النصوص."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
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
