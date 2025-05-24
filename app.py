
import streamlit as st
from core_model.model_loader import predict_with_arabbird
from web_agent.agent import analyze_with_web_agent
from utils.preprocessing import clean_text

st.set_page_config(page_title="📡 صدق.ai", layout="wide", page_icon="🤖")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        font-size: 3em;
        color: #4A90E2;
        font-weight: bold;
    }
    .subtitle {
        font-size: 1.3em;
        color: #555;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🤖 صدق.ai - Arabic Fake News Detector</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>تحليل الأخبار العربية باستخدام الذكاء الاصطناعي ووكيل بحث ويب للتحقق من الموثوقية</div>", unsafe_allow_html=True)
st.markdown("---")

option = st.radio("اختر نوع الإدخال:", ["📝 نص عربي", "🌐 رابط URL"])
input_text = st.text_area("✍️ أدخل الخبر أو الرابط:")

if st.button("🔍 تحليل الخبر"):
    if not input_text.strip():
        st.warning("⚠️ يرجى إدخال نص أو رابط.")
    else:
        with st.spinner("⏳ جاري التحليل..."):
            if option == "📝 نص عربي":
                cleaned = clean_text(input_text)
                result = predict_with_arabbird(cleaned)
                st.subheader("نتيجة النموذج 🤖")
                st.success("🟢 الخبر حقيقي" if result == 0 else "🔴 الخبر زائف")

            web_result, sources = analyze_with_web_agent(input_text)
            st.subheader("تحليل البحث عبر الإنترنت 🌐")
            st.info("🟢 موثوق" if web_result else "🔴 غير موثوق")
            if sources:
                st.markdown("### 🔗 مصادر موثوقة:")
                for src in sources:
                    st.markdown(f"- [{src['title']}]({src['url']})")
