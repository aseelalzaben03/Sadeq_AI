
import requests
from bs4 import BeautifulSoup

def analyze_with_web_agent(input_text_or_url):
    dummy_result = False
    sources = [
        {"title": "Al Jazeera", "url": "https://www.aljazeera.net"},
        {"title": "BBC Arabic", "url": "https://www.bbc.com/arabic"},
    ]
    return dummy_result, sources

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/mt5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/mt5-small")

def summarize_text_arabic(text):
    input_ids = tokenizer("تلخيص: " + text, return_tensors="pt", truncation=True, max_length=512).input_ids
    output_ids = model.generate(input_ids, max_length=100, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return summary

def get_search_query(text):
    if len(text) > 400:
        try:
            return summarize_text_arabic(text)
        except:
            return text[:300]  # fallback
    else:
        return text

def search_sources(query):
    # استخدم نفس أسلوب البحث تبعك (أنتي كنتي تستخدمي serpapi على الأغلب)
    params = {
        "engine": "google",
        "q": query,
        "api_key": "YOUR_API_KEY",
        "num": 5
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    sources = []
    for res in results.get("organic_results", []):
        sources.append({"title": res.get("title", ""), "url": res.get("link", "")})
    return sources

