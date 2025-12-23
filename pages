import streamlit as st

st.set_page_config(page_title="إضافة مرشح", layout="wide")

st.title("➕ إضافة مرشح يدويًا")

if "candidates" not in st.session_state:
    st.session_state.candidates = {}

with st.form("add_candidate"):
    name = st.text_input("👤 اسم المرشح")
    experience = st.number_input("🧠 سنوات الخبرة", min_value=0, max_value=50)
    level = st.selectbox("📊 المستوى", ["Junior", "Mid", "Senior"])
    notes = st.text_area("✍️ ملاحظات HR")

    submitted = st.form_submit_button("💾 حفظ المرشح")

if submitted:
    if not name:
        st.error("⚠️ الاسم مطلوب")
    else:
        cid = f"manual_{name}"

        st.session_state.candidates[cid] = {
            "Name": name,
            "Experience": experience,
            "Level": level,
            "Decision": "Pending",
            "Notes": notes
        }

        st.success("✅ تم إضافة المرشح")

        if st.button("⬅️ الرجوع إلى ATS"):
            st.switch_page("app.py")
