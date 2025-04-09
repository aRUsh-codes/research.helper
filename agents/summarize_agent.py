from utils.gemini_utils import get_gemini_response

def summarize_text(text, max_tokens=1000):
    prompt = f"""
    You are an expert AI researcher. Summarize the following academic paper text in a clear, concise way:
    ===
    {text[:5000]}
    ===
    Provide a crisp summary under {max_tokens} tokens.
    """
    return get_gemini_response(prompt)
