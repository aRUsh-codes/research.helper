import streamlit as st
from dotenv import load_dotenv
import os
import tempfile
from gtts import gTTS

# Agents
from utils.gemini_utils import setup_gemini
from agents.ingest_agent import extract_text_from_pdf, extract_text_from_url_pdf
from agents.summarize_agent import summarize_text
from agents.classify_agent import classify_text
from agents.search_agent import search_papers_arxiv
from agents.doi_agent import fetch_metadata_from_doi
from agents.synthesis_agent import topic_synthesis_flow

# Load environment
load_dotenv(dotenv_path=".env.local")
api_key = os.getenv("GEMINI_API_KEY")

# Configure app
st.set_page_config(page_title="AI Research Paper Summarizer", layout="wide")
st.title("AI Research Paper Summarizer with Gemini")

# Setup Gemini
if api_key:
    setup_gemini(api_key)
else:
    st.error("No Gemini API key found. Please check your .env.local file.")
    st.stop()


# ------------------------------------------
#  Sidebar Navigation
# ------------------------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    [
        "📄 PDF Summarization",
        "🌐 URL/DOI Ingestion",
        "🔍 Search Papers",
        "📡 Topic-based Synthesis"
    ]
)

# ------------------------------------------
# PDF Summarization
# ------------------------------------------
if section == "📄 PDF Summarization":
    st.header("📄 Upload & Summarize Research Paper (PDF)")

    uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")
    use_sample = st.button("📎 Use Sample PDF")

    # Extract and store PDF text (uploaded or sample)
    if uploaded_file:
        paper_text = extract_text_from_pdf(uploaded_file)
        st.session_state["paper_text"] = paper_text
        st.success("Text extracted from uploaded PDF.")

    elif use_sample:
        try:
            with open("sample_data/sample.pdf", "rb") as f:
                paper_text = extract_text_from_pdf(f)
                st.session_state["paper_text"] = paper_text
                st.success("Sample PDF loaded and text extracted.")
        except FileNotFoundError:
            st.error("Sample PDF not found. Please add it to sample_data/sample.pdf.")

    # Summarization
    if "paper_text" in st.session_state:
        if st.button("Summarize PDF"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(st.session_state["paper_text"])
                st.subheader("Summary:")
                st.write(summary)

                st.subheader("🎧Listen to Summary:")
                tts = gTTS(summary)
                with tempfile.NamedTemporaryFile(delete=True) as fp:
                    tts.save(fp.name + ".mp3")
                    audio_file = open(fp.name + ".mp3", "rb")
                    st.audio(audio_file.read(), format='audio/mp3')

        st.subheader("Topic Classification")
        topics = st.text_input("Enter comma-separated topic list",
                               value="NLP, Computer Vision, Reinforcement Learning, LLMs, Healthcare AI")
        if st.button("Classify"):
            with st.spinner("Classifying..."):
                topic_list = [t.strip() for t in topics.split(",")]
                classification = classify_text(st.session_state["paper_text"], topic_list)
                st.markdown("**Predicted Topics:**")
                st.success(classification)
    else:
        st.info("Upload a PDF or use the sample to get started.")


# ------------------------------------------
# URL/DOI Ingestion
# ------------------------------------------
elif section == "🌐 URL/DOI Ingestion":
    st.header("🌐 Ingest Paper via PDF URL or DOI")

    with st.expander("Ingest from PDF URL"):
        url_input = st.text_input("Enter direct PDF URL or Use Sample Link")

        sample_link = "https://www.jetir.org/papers/JETIR2107018.pdf"

        use_sample_link = st.button("🔗Use Sample Link")
        if use_sample_link:
            url_input = sample_link
            st.success("Sample link loaded.")
        
        if st.button("Ingest PDF from URL"):
            if url_input:
                try:
                    paper_text = extract_text_from_url_pdf(url_input)
                    st.session_state["url_paper_text"] = paper_text
                    st.success("PDF text extracted. Ready to summarize.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter a valid PDF URL.")

        if "url_paper_text" in st.session_state:
            if st.button("Summarize URL Paper"):
                with st.spinner("Summarizing..."):
                    summary = summarize_text(st.session_state["url_paper_text"])
                    st.subheader("Summary:")
                    st.write(summary)

                    st.subheader("🎧Listen to Summary:")
                    tts = gTTS(summary)
                    with tempfile.NamedTemporaryFile(delete=True) as fp:
                        tts.save(fp.name + ".mp3")
                        audio_file = open(fp.name + ".mp3", "rb")
                        st.audio(audio_file.read(), format='audio/mp3')


    with st.expander("Ingest from DOI"):
        doi_input = st.text_input("Enter a DOI (e.g. 10.48550/arXiv.2205.09713)")

        if st.button("Fetch from DOI"):
            if doi_input:
                try:
                    meta = fetch_metadata_from_doi(doi_input)

                    # Always show metadata regardless of PDF link availability
                    st.markdown(f"### {meta.get('title', 'Title not found')}")
                    st.markdown(f"**Authors:** {', '.join(meta.get('authors', [])) or 'Authors not found'}")
                    st.markdown("**Abstract:**")
                    st.write(meta.get("abstract", "Abstract not found."))

                    # Only then check if full-text PDF is available
                    if meta["link"]:
                        st.success("PDF found! Extracting content...")
                        paper_text = extract_text_from_url_pdf(meta["link"])
                        st.session_state["doi_paper_text"] = paper_text
                    else:
                        st.warning("Full-text PDF not available via CrossRef. Only metadata shown.")

                except Exception as e:
                    st.error(f"Error fetching from DOI: {e}")
            else:
                st.warning("Please enter a valid DOI.")

        if "doi_paper_text" in st.session_state:
            if st.button("Summarize DOI Paper"):
                summary = summarize_text(st.session_state["doi_paper_text"])
                st.subheader("Summary:")
                st.write(summary)

                st.subheader("🎧Listen to Summary:")
                tts = gTTS(summary)
                with tempfile.NamedTemporaryFile(delete=True) as fp:
                    tts.save(fp.name + ".mp3")
                    audio_file = open(fp.name + ".mp3", "rb")
                    st.audio(audio_file.read(), format='audio/mp3')

# ------------------------------------------
#  Search Papers
# ------------------------------------------
elif section == "🔍 Search Papers":
    st.header("🔍 Search Research Papers (arXiv)")

    search_query = st.text_input("Enter a topic or keyword (e.g. Transformers)")
    max_results = st.slider("Number of results", 1, 10, 5)
    sort_option = st.selectbox("Sort by", ["relevance", "recency"])

    if st.button("Search"):
        try:
            papers = search_papers_arxiv(search_query, max_results=max_results, sort_by=sort_option)
            if papers:
                for paper in papers:
                    st.markdown(f"### {paper['title']}")
                    st.markdown(f"- **Published:** {paper['published']}")
                    st.markdown(f"- **Authors:** {', '.join(paper['authors'])}")
                    st.markdown(f"- **Summary:** {paper['summary'][:500]}...")
                    st.markdown(f"[🔗 Full PDF]({paper['pdf_url']})")
                    st.markdown("---")
            else:
                st.warning("No results found.")
        except Exception as e:
            st.error(f"Error searching: {e}")

# ------------------------------------------
#   Cross-Paper Topic Synthesis
# ------------------------------------------
elif section == "📡 Topic-based Synthesis":
    st.header("📡 Cross-Paper Synthesis by Topic")

    cross_topic = st.text_input("Enter topic to synthesize (e.g. Contrastive Learning)")
    cross_count = st.slider("Number of papers to synthesize", 2, 10, 3)

    if st.button("Run Topic Synthesis"):
        if not cross_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Synthesizing from multiple papers..."):
                try:
                    synthesis_output, paper_list = topic_synthesis_flow(cross_topic, cross_count)

                    st.subheader(" Synthesized Insight:")
                    st.write(synthesis_output)

                    st.subheader("🎧Listen to Synthesis:")
                    tts = gTTS(synthesis_output)
                    with tempfile.NamedTemporaryFile(delete=True) as fp:
                        tts.save(fp.name + ".mp3")
                        audio_file = open(fp.name + ".mp3", "rb")
                        st.audio(audio_file.read(), format='audio/mp3')

                    st.subheader("Papers Used:")
                    for p in paper_list:
                        st.markdown(f"**{p['title']}**")
                        st.markdown(f"- Authors: {', '.join(p['authors'])}")
                        st.markdown(f"- Published: {p['published']}")
                        st.markdown(f"[🔗 Read PDF]({p['url']})")
                        st.markdown("---")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
