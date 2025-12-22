import streamlit as st
import pandas as pd
import docx
import PyPDF2
import re
from datetime import datetime

st.set_page_config(page_title="🤖 محلل خبرات ذكي", layout="wide")
st.title("🤖 محلل خبرات السير الذاتية (بدون AI)")
st.write("يرفع السيرة الذاتية ويحسب سنوات الخبرة من التواريخ كأنه إنسان حقيقي.")

uploaded_files = st.file_uploader("ارفع السير الذاتية", accept_multiple_files=True)

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

# ---------- تحويل الشهور ----------
MONTHS = {
    "jan":1,"january":1,"يناير":1,
    "feb":2,"february":2,"فبراير":2,
    "mar":3,"march":3,"مارس":3,
    "apr":4,"april":4,"أبريل":4,
    "may":5,"مايو":5,
    "jun":6,"june":6,"يونيو":6,
    "jul":7,"july":7,"يوليو":7,
    "aug":8,"august":8,"أغسطس":8,
    "sep":9,"september":9,"سبتمبر":9,
    "oct":10,"october":10,"أكتوبر":10,
    "nov":11,"november":11,"نوفمبر":11,
    "dec":12,"december":12,"ديسمبر":12,
}

def parse_date(text):
    text = text.lower().strip()

    if text in ["present", "now", "الآن", "حتى الآن"]:
        return datetime.today()

    # سنة فقط
    if re.fullmatch(r"\d{4}", text):
        return datetime(int(text), 1, 1)

    # شهر + سنة
    for m in MONTHS:
        if m in text:
            year = re.search(r"\d{4}", text)
            if year:
                return datetime(int(year.group()), MONTHS[m], 1)

    return None

# ---------- استخراج الفترات ----------
def extract_periods(text):
    text = text.replace("–", "-").replace("—", "-")
    patterns = [
        r"(.{3,15})\s*-\s*(present|now|الآن|حتى الآن|\d{4}|.{3,15})",
        r"from\s+(.{3,15})\s+to\s+(.{3,15})",
        r"من\s+(.{3,15})\s+إلى\s+(.{3,15})",
    ]

    periods = []

    for pattern in patterns:
        for match in re.findall(pattern, text, re.IGNORECASE):
            start = parse_date(match[0])
            end = parse_date(match[1])
            if start and end and end > start:
                periods.append((start, end))

    return periods

# ---------- حساب السنوات ----------
def calculate_years(periods):
    total_days = sum((end - start).days for start, end in periods)
    return round(total_days / 365, 1)

# ---------- التنفيذ ----------
if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 {file.name}")
        text = extract_text(file)

        periods = extract_periods(text)
        if periods:
            years = calculate_years(periods)
            st.success(f"🧠 سنوات الخبرة المحسوبة: {years} سنة")

            with st.expander("عرض الفترات المستخرجة"):
                for s, e in periods:
                    st.write(f"{s.date()} → {e.date()}")
        else:
            st.warning("❌ لم أستطع استخراج فترات خبرة واضحة من السيرة")
