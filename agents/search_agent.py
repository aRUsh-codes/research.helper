import arxiv

def search_papers_arxiv(query, max_results=5, sort_by="relevance"):
    sort = arxiv.SortCriterion.Relevance if sort_by == "relevance" else arxiv.SortCriterion.SubmittedDate
    results = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=sort,
        sort_order=arxiv.SortOrder.Descending
    )
    papers = []
    for r in results.results():
        papers.append({
            "title": r.title,
            "summary": r.summary,
            "pdf_url": r.pdf_url,
            "published": r.published.strftime("%Y-%m-%d"),
            "authors": [a.name for a in r.authors]
        })
    return papers
