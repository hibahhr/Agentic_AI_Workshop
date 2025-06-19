import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from dotenv import load_dotenv

# import agents to the main script
from agents.startup_interpreter import interpret_startup
from agents.kpi_critique import critique_kpis_with_llm
from agents.impact_kpi_retriever import retrieve_impact_kpis
from agents.real_world_kpi_recommender import recommend_kpis_from_web
from agents.insight_visualizer import display_kpi_dashboard


os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
load_dotenv()
os.makedirs("papers", exist_ok=True)

# Setup LLM and tavily
print("\nSetting up LLM and web search client...")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    temperature=0.2,
    convert_system_message_to_human=True)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Load and chunk PDF documents
print("\nLoading and chunking documents...")
loader = PyPDFDirectoryLoader("./papers")
pages = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(pages)
print(f"Loaded {len(pages)} pages and split into {len(chunks)} chunks.")

# Generate embeddings and store in Chroma vectorstore
print("\nGenerating embeddings and storing in Chroma vector store...")
vectorstore = None
try:
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False}
    )

    print("Embedding model loaded.")
    vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory="rag_db")
    print("Vectorstore created from documents.")
    vectorstore.persist()
    print("Embeddings persisted to rag_db/")
except Exception as e:
    print("Error during embedding/vectorstore step:", e)
    exit()

# Build the RAG retriever chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"
)

# Sample startup info
startup_info = {
    "type": "Marketplace",
    "stage": "Seed",
    "user_kpis": ["App Downloads", "GMV", "Instagram Likes", "Active Sellers", "User Retention Rate"]
}

# Run agents
print("\nStep 1: Interpreting Startup...")
interpretation = interpret_startup(startup_info, llm, tavily)
print("Interpreted Startup KPI Focus:", interpretation)

print("\nStep 2: Critiquing User KPIs...")
critique_result = critique_kpis_with_llm(startup_info["user_kpis"], interpretation, llm)
print("KPI Classification:")
for kpi, feedback in critique_result.items():
    print(f"- {kpi}: {feedback}")

print("\nStep 3: Retrieving RAG-based Impact KPIs...")
rag_impact_kpis = retrieve_impact_kpis(interpretation, qa_chain)
print("RAG-based Impact KPI Suggestions:")
for kpi in rag_impact_kpis:
    print(f"- {kpi}")

print("\nStep 4: Getting Real-World KPI Suggestions via Web...")
real_world_kpis = recommend_kpis_from_web(interpretation, critique_result, rag_impact_kpis, llm, tavily)
print("Real-World KPI Suggestions (via Tavily):")
for kpi in real_world_kpis:
    print(f"- {kpi}")
    
print("\nStep 5: Visualizing KPIs in Dashboard...")
display_kpi_dashboard(critique_result, rag_impact_kpis, real_world_kpis)


print("\nAll agents ran successfully!")
