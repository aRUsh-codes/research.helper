# utils/gemini_utils.py
import google.generativeai as genai
import os

def setup_gemini(api_key):
    genai.configure(api_key=api_key)

def get_gemini_response(prompt, temperature=0.7, model="models/gemini-1.5-pro-latest"):
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    return response.text

def list_available_models(api_key):
    genai.configure(api_key=api_key)
    models = genai.list_models()
    for m in models:
        print(m.name, m.supported_generation_methods)