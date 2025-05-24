
import requests
from bs4 import BeautifulSoup

def analyze_with_web_agent(input_text_or_url):
    dummy_result = False
    sources = [
        {"title": "Al Jazeera", "url": "https://www.aljazeera.net"},
        {"title": "BBC Arabic", "url": "https://www.bbc.com/arabic"},
    ]
    return dummy_result, sources
