from agents.search_agent import search_papers_arxiv
from agents.summarize_agent import summarize_text
from utils.gemini_utils import get_gemini_response

def synthesize_multiple_summaries(summaries, topic):
    combined = "\n\n".join([f"Paper {i+1}: {s}" for i, s in enumerate(summaries)])
    
    prompt = f"""
    You are an AI research summarizer. You have been given summaries of multiple research papers on the topic of '{topic}'.

    Your job is to:
    - Identify common themes
    - Point out differences in approach or findings
    - Provide a 2–3 paragraph synthesis that gives the reader a clear overview of what the research landscape looks like for this topic.

    === PAPER SUMMARIES ===
    {combined}
    """
    return get_gemini_response(prompt)


def topic_synthesis_flow(topic, num_papers=3):
    papers = search_papers_arxiv(topic, max_results=num_papers)
    summaries = []
    used_papers = []

    for paper in papers:
        summary = summarize_text(paper['summary'])  # summarizing arXiv's abstract
        summaries.append(summary)
        used_papers.append({
            "title": paper['title'],
            "url": paper['pdf_url'],
            "authors": paper['authors'],
            "published": paper['published']
        })

    synthesis = synthesize_multiple_summaries(summaries, topic)
    return synthesis, used_papers
