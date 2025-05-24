

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "Aseelalzaben03/sadaqai-bestmodel"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def predict_with_arabbird(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
    return prediction
