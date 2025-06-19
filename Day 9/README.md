# KPI Intelligence Suite for Startups 

This project is an intelligent, LLM-driven suite designed to help early-stage startups identify, critique, and visualize their most relevant **Key Performance Indicators (KPIs)** using a combination of RAG (Retrieval-Augmented Generation), web data, and domain-specific knowledge.

## Features

- **Interpret Startup Context**  
  Uses LLM and web research (via Tavily) to derive the core metric focus based on startup type and stage.

- **Critique Submitted KPIs**  
  Classifies user-provided KPIs as "Vanity" or "Impact" using an expert LLM critique engine.

- **Retrieve Impact KPIs (RAG)**  
  Suggests industry-standard KPIs using a custom document retriever powered by LangChain and HuggingFace embeddings.

- **Recommend Real-World KPIs**  
  Gathers practical KPIs from live web sources using Tavily for grounded relevance.

- **Insight Visualizer Dashboard**  
  Generates a visual dashboard to help founders differentiate between vanity and impact metrics using Plotly and Gradio.

---

## Project Structure

```

.
├── agents/
│   ├── impact\_kpi\_retriever.py
│   ├── insight\_visualizer.py
│   ├── kpi\_critique.py
│   ├── real\_world\_kpi\_recommender.py
│   └── startup\_interpreter.py
├── papers/                # PDF documents here (for RAG)
├── rag\_db/               # Auto-generated vector database
├── .env                   # Environment variables (Tavily, Google Gemini, HuggingFace, etc.)
├── main.py                # Entry point script to run the entire pipeline
└── README.md              # You're here!

````

---

## Tech Stack

- **LangChain** – RAG and LLM integration
- **Google Gemini** – LLM for interpretation and critique
- **Tavily API** – Web-based KPI recommendations
- **Gradio + Plotly** – Interactive dashboard for KPI insights
- **ChromaDB + HuggingFace Embeddings** – Vectorstore for RAG

---

## Notes

* Requires **Python 3.8+**
* The Gradio dashboard will launch in your browser after successful execution.
* API keys are required for Tavily and Google Gemini (via LangChain integration).

---