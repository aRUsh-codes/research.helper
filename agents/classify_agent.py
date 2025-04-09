from utils.gemini_utils import get_gemini_response

def classify_text(text,topic_list,max_tokens=1000):
    prompt = f"""
    You are a research assistant.
    Given the content of the research academic paper. Classify it into one or more of the following topics.
    
    {topic_list}
    
    Only return the relevant topic names that matcch the content of the paper.
    
    Here is the paper content.
    {text[:5000]}
    """
    return get_gemini_response(prompt)
    