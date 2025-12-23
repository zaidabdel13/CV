import streamlit as st
import pandas as pd
import docx
import PyPDF2
import re
from datetime import datetime

# ================= إجبار إعادة التحميل =================
st.markdown("<!-- FORCE RELOAD -->", unsafe_allow_html=True)

# ================= إعداد الصفحة =================
st.set_page_config(
    page_title="ATS | HR System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= CSS واجهة HR =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #3b0d12 0%, #120002 70%);
    color: #f2f2f2;
    font-family: 'Segoe UI', sans-serif;
}
.stApp::before {
    content:"";
    position:fixed;
    inset:0;
    background:
      radial-gradient(circle at 20% 10%, rgba(255,255,255,0.08), transparent 40%),
      radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05), transparent 45%);
    pointer-events:none;
}
h1,h2,h3 { color:#ffd6d6; letter-spacing:1px; }

.card {
    background: rgba(20,0,0,0.75);
    border: 1px solid rgba(255,90,90,0.25);
    border-radius:16px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 0 30px rgba(0,0,0,0.6);
}

.badge { font-weight:700; font-size:18px; }
.junior { color:#ff7675; }
.mid { color:#fdcb6e; }
.senior { color:#00b894; }

.status {
    font-size:16px;
    font-weight:bold;
    padding:6px 16px;
    border-radius:20px;
    display:inline-block;
    margin-top:8px;
}
.accepted { background:#1b5e20; color:#b9f6ca; }
.rejected { background:#7f0000; color:#ffcdd2; }
.hold { background:#6d4c41; color:#ffe0b2; }
.pending { background:#424242; color:#eeeeee; }

footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ================= العنوان =================
st.markdown("<h1>🧑‍💼 ATS – Applicant Tracking System</h1>", unsafe_allow_html=True)
st.markdown("نظام تتبع المتقدمين – واجهة HR احترافية")

# ================= زر إضافة مرشح =================
if st.button("➕ إضافة مرشح يدويًا"):
    st.switch_page("pages/1_Add_Candidate.py")

# ================= Session =================
if "candidates" not in st.session_state:
    st.session_state.candidates = {}   # dict لمنع التكرار

# ================= رفع الملفات =================
uploaded_files = st.file_uploader(
    "📄 ارفع السير الذاتية (PDF / Word / Excel)",
    accept_multiple_files=True
)

# ================= أدوات القراءة =================
def extract_text(file):
    name = file.name.lower()
    if name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    if name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    if name.endswith((".xlsx",".xls")):
        df = pd.read_excel(file)
        return df.to_string()
    return ""

def extract_years(text):
    return sorted(set(int(y) for y in re.findall(r'\b(19\d{2}|20\d{2})\b', text)))

def calc_experience(years):
    if len(years) < 2:
        return 0
    return min(datetime.now().year, max(years)) - min(years)

def classify(exp):
    if exp <= 2: return "Junior", "junior"
    if exp <= 6: return "Mid", "mid"
    return "Senior", "senior"

# ================= معالجة الملفات =================
if uploaded_files:
    for f in uploaded_files:
        cid = f"{f.name}_{f.size}"

        if cid not in st.session_state.candidates:
            text = extract_text(f)
            years = extract_years(text)
            exp = calc_experience(years)
            lvl, _ = classify(exp)

            st.session_state.candidates[cid] = {
                "Name": f.name,
                "Experience": exp,
                "Level": lvl,
                "Decision": "Pending",
                "Notes": ""
            }

# ================= عرض المرشحين =================
st.markdown("## 📂 المرشحين")

for cid, c in st.session_state.candidates.items():
    lvl, css = classify(c["Experience"])

    st.markdown(f"""
    <div class="card">
      <h3>📄 {c['Name']}</h3>
      <div class="badge {css}">
        🧠 الخبرة: {c['Experience']} سنوات – {lvl}
      </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Accept", key=f"a_{cid}"):
            c["Decision"] = "Accepted"
    with col2:
        if st.button("❌ Reject", key=f"r_{cid}"):
            c["Decision"] = "Rejected"
    with col3:
        if st.button("⏸ Hold", key=f"h_{cid}"):
            c["Decision"] = "Hold"

    c["Notes"] = st.text_area("✍️ ملاحظات HR", c["Notes"], key=f"n_{cid}")

    status_class = {
        "Accepted": "accepted",
        "Rejected": "rejected",
        "Hold": "hold",
        "Pending": "pending"
    }[c["Decision"]]

    st.markdown(
        f"<div class='status {status_class}'>📌 {c['Decision']}</div>",
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ================= Dashboard =================
if st.session_state.candidates:
    st.markdown("## 📊 Dashboard")
    df = pd.DataFrame(st.session_state.candidates.values())

    c1,c2,c3 = st.columns(3)
    c1.metric("👥 المرشحين", len(df))
    c2.metric("🟢 مقبولين", (df["Decision"]=="Accepted").sum())
    c3.metric("🔴 مرفوضين", (df["Decision"]=="Rejected").sum())

    st.bar_chart(df["Level"].value_counts())

    st.download_button(
        "📥 تصدير Excel",
        df.to_csv(index=False).encode("utf-8-sig"),
        "ATS_Report.csv",
        "text/csv"
    )
