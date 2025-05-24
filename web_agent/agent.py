# WebAgent/agent.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from googlesearch import search
import torch

# تحميل نموذج mT5 من HuggingFace
tokenizer = AutoTokenizer.from_pretrained("google/mt5-small", use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained("google/mt5-small")

def summarize_text(text):
    """تلخيص النص العربي باستخدام mT5"""
    input_ids = tokenizer("تلخيص: " + text, return_tensors="pt", truncation=True, max_length=512).input_ids
    summary_ids = model.generate(input_ids, max_length=100, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def get_sources(query, num_results=5):
    """البحث عن مصادر عربية في Google"""
    try:
        results = list(search(query, lang="ar", num_results=num_results))
        return results
    except Exception as e:
        return ["حدث خطأ أثناء البحث:", str(e)]

def web_agent_analysis(text):
    """
    المهمة الرئيسية: تلخيص النص، البحث عنه، إرجاع المصادر وثقة النتيجة
    """
    summary = summarize_text(text)
    sources = get_sources(summary)

    # حساب نسبة الثقة بناءً على عدد المصادر
    confidence = round(min(len(sources) / 5, 1.0), 2)

    result = {
        "summary": summary,
        "sources": sources,
        "confidence": confidence
    }
    return result

# مثال تشغيل مباشر
if __name__ == "__main__":
    input_text = "أعلنت وزارة الصحة الأردنية عن بدء توزيع لقاحات جديدة في جميع المستشفيات الحكومية مجانًا."
    result = web_agent_analysis(input_text)

    print("💡 ملخص الذكاء الصناعي:\n", result["summary"])
    print("\n🔎 مصادر موثوقة:")
    for link in result["sources"]:
        print("-", link)
    print("\n🔒 نسبة الثقة:", result["confidence"])

