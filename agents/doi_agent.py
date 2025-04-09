import requests

def fetch_metadata_from_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["message"]
        metadata = {
            "title": data.get("title", [""])[0],
            "authors": [author["family"] + ", " + author["given"] for author in data.get("author", [])],
            "abstract": data.get("abstract", "Abstract not available"),
            "link": next((link["URL"] for link in data.get("link", []) if link.get("content-type") == "application/pdf"), None)
        }
        return metadata
    else:
        raise Exception("DOI not found or CrossRef API error.")
