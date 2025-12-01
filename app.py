import streamlit as st
import google.generativeai as genai
import base64

st.set_page_config(page_title="Fahman - فهمان", page_icon="logo.png", layout="centered")

def encode_img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = encode_img("background.jpg")
logo_main = encode_img("logo.png")
logo_small = encode_img("SLogo.png")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg}");
        background-size: cover;
        background-position: center;
    }}

    .glass-container {{
        background: rgba(255,255,255,0.35);
        padding: 40px;
        border-radius: 25px;
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.4);
        max-width: 850px;
        margin: auto;
        margin-top: 20px;
    }}

    .title {{
        text-align:center;
        font-family:Tahoma;
        color:black;
        font-size:42px;
        margin-top:-10px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }}

    .center-logo {{
        display: flex;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }}

    .footer {{
        text-align:center;
        margin-top:35px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='glass-container'>", unsafe_allow_html=True)

st.markdown(f"<div class='center-logo'><img src='data:image/png;base64,{logo_main}' width='230'></div>", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🤖 فهمان – خبير المسارات التعليمية</h1>", unsafe_allow_html=True)

st.write("اكتب أي تراك عايز تتعلمه، وفهمان هيبني لك Roadmap + مصادر.")

GENAI_KEY = "AIzaSyCQs_eYt7yGFZR-vYkwEE-E9bAhw6T4JnI"
genai.configure(api_key=GENAI_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

SOURCES = {
    "ai": [
        ("Machine Learning Specialization – Andrew Ng", "Coursera"),
        ("Deep Learning Specialization – Andrew Ng", "Coursera"),
        ("fast.ai Practical Deep Learning", "Course"),
        ("CS229 – Stanford Machine Learning Notes", "Stanford"),
        ("Hands-On Machine Learning – Aurélien Géron", "Book")
    ],
    "python": [
        ("Python for Everybody – Dr. Charles", "Coursera"),
        ("Automate the Boring Stuff with Python", "Book"),
        ("Corey Schafer YouTube Python Playlist", "YouTube")
    ],
    "flutter": [
        ("Flutter & Dart - Angela Yu", "Udemy"),
        ("Official Flutter Documentation", "flutter.dev"),
        ("The Net Ninja Flutter Course", "YouTube")
    ],
    "cyber": [
        ("TryHackMe Complete Path", "TryHackMe"),
        ("CompTIA Security+ SY0-701", "Cert"),
        ("Cybrary SOC Analyst Path", "Cybrary")
    ]
}

def get_sources(track):
    track = track.lower()
    for key in SOURCES:
        if key in track:
            return SOURCES[key]
    return []

def generate_roadmap(track, sources):
    prompt = f"""
أنت خبير تعليمي اسمه "فهمان". مهمتك عمل Roadmap واضحة وبروفيشنال لتراك: {track}.
أريد أن يكون الرد بهذا الشكل:
1) مقدمة قصيرة.
2) خطة تعليمية مقسمة مراحل (مبتدئ – متوسط – محترف).
3) لكل مرحلة: المهارات المطلوبة + ما يجب تعلمه + مشاريع مقترحة.
4) مصادر تعلم موثوقة (من اللي عندي + إن احتجت أضف من عندك).
5) جدول أسبوعي مقترح.
6) نصائح للمبتدئين.
المصادر الجاهزة المتاحة لك هي:
{sources}
اكتب بأسلوب احترافي ومختصر وعملي.
    """
    response = model.generate_content(prompt)
    return response.text

user_track = st.text_input("🎯 اكتب التراك اللي عايز تتعلمه:")

if st.button("🔍 تحليل وبناء Roadmap"):
    if not user_track.strip():
        st.warning("اكتب تراك الأول 🙏")
    else:
        with st.spinner("فهمان بيفكر..."):
            found_sources = get_sources(user_track)
            src_text = "\n".join([f"- {s[0]} ({s[1]})" for s in found_sources]) if found_sources else "لا توجد مصادر."
            final_answer = generate_roadmap(user_track, src_text)

        st.subheader("📌 خطة فهمان:")
        st.write(final_answer)

        if found_sources:
            st.subheader("📚 مصادر مقترحة:")
            for title, src in found_sources:
                st.write(f"- **{title}** — {src}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class='footer'>
        <img src='data:image/png;base64,{logo_small}' width='85'>
        <p style='color:white; font-size:18px; text-shadow:1px 1px 4px #000'>Powered by AI Spark ACU</p>
    </div>
    """,
    unsafe_allow_html=True
)
