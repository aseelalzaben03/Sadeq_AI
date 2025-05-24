# main.py

from model.model_loader import load_model_and_tokenizer, predict_label
from WebAgent.agent import web_agent_analysis

import torch

# تحميل النموذج المدرب
model, tokenizer = load_model_and_tokenizer()

def combined_analysis(text):
    # 🔮 التنبؤ من النموذج المدرب
    prediction, confidence_model = predict_label(text, model, tokenizer)

    # 🌐 نتيجة Web Search Agent
    web_result = web_agent_analysis(text)
    confidence_web = web_result["confidence"]

    # 🧠 دمج النتائج
    combined_confidence = round((confidence_model + confidence_web) / 2, 2)

    if confidence_model > confidence_web:
        final_label = prediction  # خذ رأي النموذج إذا كان واثق أكثر
    else:
        final_label = "Fake" if prediction == "Real" else "Real"  # عكس تنبؤ النموذج إذا المصادر قليلة

    return {
        "final_decision": final_label,
        "model_prediction": prediction,
        "model_confidence": confidence_model,
        "web_confidence": confidence_web,
        "combined_confidence": combined_confidence,
        "web_sources": web_result["sources"],
        "summary": web_result["summary"]
    }

# مثال تشغيل
if __name__ == "__main__":
    text = "أعلنت الحكومة عن إطلاق تطبيق مجاني لتوزيع الأدوية على المواطنين عبر الإنترنت."
    result = combined_analysis(text)

    print(f"\n✅ القرار النهائي: {result['final_decision']} ({result['combined_confidence'] * 100:.1f}%)")
    print(f"🔍 توقع النموذج: {result['model_prediction']} ({result['model_confidence'] * 100:.1f}%)")
    print(f"🌐 ثقة المصادر: {result['web_confidence'] * 100:.1f}%")
    print(f"📝 ملخص البحث: {result['summary']}")
    print("📚 مصادر البحث:")
    for link in result["web_sources"]:
        print("-", link)
