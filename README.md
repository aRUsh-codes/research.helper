# Agent Research

Ever felt lost trying to keep up with all the new research and tech advancements?  
**Agent Research** is here to make that easier.

Using advanced LLM capabilities, web search integration, and a multi-agent architecture, **Agent Research** can:

1. Search the web for up to 10 research papers on any topic, with filtering options like recency and relevance.
2. Summarize complex, jargon-heavy research papers into simple language.  
   Don’t feel like reading? You can even listen to the summary like a podcast.
3. Analyze any research paper from just its **PDF URL or DOI** — showing you the summary, authors, and publish date.
4. Use multi-agent synthesis to combine insights from multiple papers and generate a unified explanation.  
   For example, it can answer: _"Why do Transformers need attention?"_ based on collective research.

---

## ⚙️ Tech Used

- **Streamlit** – for building the interactive UI
- **Gemini API (Google Generative AI)** – for summarization, classification, and synthesis
- **PyMuPDF** – for PDF text extraction
- **arXiv API** – for research paper discovery
- **CrossRef API** – for DOI metadata retrieval
- **gTTS (Google Text-to-Speech)** – to generate audio summaries
- **Requests** – to fetch content via URLs

---

## 🚀 Want to Get Started?

Try the hosted app directly
[here](https://agentresearch.streamlit.app/)

---

## 🛠️ Want to Contribute / Run Locally?

1. Clone or fork the repo
2. Create a virtual environment and install dependencies using ```pip install -r requirements.txt```
3. Create a .env.local file and add this: ```GEMINI_API_KEY=your_key_here```
4. Run the app: ```streamlit run app.py```


## 🎥 Working Demo


https://github.com/user-attachments/assets/e8c1e186-6d53-4aea-8ce4-ad2d21e05646



## 🧩 Limitations and Future Scope

1. **User Authentication & Personalization**:  
   Currently, the app does not store user data. A future version could include authentication and user-specific storage to retain their search history, saved summaries, and preferences.

2. **Enhanced Audio Podcast Features**:  
   The current audio is generated using a basic TTS engine. Future improvements could include multi-language support, custom voices, tone variation, and podcast-style narration.

3. **Smarter DOI Processing**:  
   While basic DOI-based extraction works, a more advanced system could directly fetch and process full research papers from various publishers and repositories using just the DOI, even in restricted access scenarios.

   
