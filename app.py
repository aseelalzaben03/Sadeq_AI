
import streamlit as st
from core_model.model_loader import predict_with_arabbird
from web_agent.agent import analyze_with_web_agent
from utils.preprocessing import clean_text

st.set_page_config(page_title="📡 صدق.ai", layout="wide", page_icon="🤖")

st.markdown("""
    <style>
    /* ضبط اتجاه الصفحة للغة العربية من اليمين إلى اليسار */
    .main {
        background-color: #ffcccc;
        color: #333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
        text-align: right;
        position: relative;
        min-height: 100vh;
        padding: 20px 40px;
        overflow-x: hidden;
    }
    /* كتابة خافتة كبيرة كخلفية */
    .main::before {
        content: "صدق AI S-A-D-E-Q-A-I";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 7em;
        color: rgba(255, 255, 255, 0.15);
        font-weight: 900;
        letter-spacing: 0.5em;
        user-select: none;
        pointer-events: none;
        white-space: nowrap;
        z-index: 0;
    }
    /* العنوان */
    .title {
        font-size: 3em;
        color: #b22222; /* لون أحمر داكن */
        font-weight: 900;
        margin-bottom: 0.1em;
        z-index: 1;
        position: relative;
    }
    /* العنوان الفرعي */
    .subtitle {
        font-size: 1.5em;
        color: #800000; /* أحمر داكن */
        margin-bottom: 1em;
        font-weight: 600;
        z-index: 1;
        position: relative;
    }
    /* تصميم الزر */
    .stButton>button {
        background-color: #b22222;
        color: white;
        font-size: 20px;
        padding: 12px 28px;
        border-radius: 12px;
        border: none;
        font-weight: 700;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #800000;
    }
    /* صندوق النص */
    textarea, input[type="text"] {
        font-size: 1.1em;
        padding: 10px;
        border-radius: 8px;
        border: 1.5px solid #b22222;
        direction: rtl;
        text-align: right;
    }
    /* خيار الراديو */
    .css-1gk9f4s {
        flex-direction: row-reverse !important;
        justify-content: flex-start !important;
    }
    /* قسم النتائج */
    .results-section {
        background: rgba(255, 255, 255, 0.9);
        padding: 15px 20px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(178, 34, 34, 0.3);
        z-index: 1;
        position: relative;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🤖 صدق.ai - كاشف الأخبار الزائفة بالعربية</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>تحليل الأخبار باستخدام الذكاء الاصطناعي ووكيل بحث ويب للتحقق من الموثوقية</div>", unsafe_allow_html=True)
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
                st.markdown("<div class='results-section'>", unsafe_allow_html=True)
                st.subheader("نتيجة النموذج 🤖")
                st.success("🟢 الخبر حقيقي" if result == 0 else "🔴 الخبر زائف")
                st.markdown("</div>", unsafe_allow_html=True)

            web_result, sources = analyze_with_web_agent(input_text)
            st.markdown("<div class='results-section'>", unsafe_allow_html=True)
            st.subheader("تحليل البحث عبر الإنترنت 🌐")
            st.info("🟢 موثوق" if web_result else "🔴 غير موثوق")
            if sources:
                st.markdown("### 🔗 مصادر موثوقة:")
                for src in sources:
                    st.markdown(f"- [{src['title']}]({src['url']})")
            st.markdown("</div>", unsafe_allow_html=True)
