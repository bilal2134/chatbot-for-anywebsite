import os
import hashlib
from pathlib import Path
from pinecone import Pinecone
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import StorageContext, VectorStoreIndex, download_loader
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load API keys from environment
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Data source URL
DATA_URL = "https://www.gettingstarted.ai/how-to-use-gemini-pro-api-llamaindex-pinecone-index-to-build-rag-app"

# Initialize models with the updated libraries
llm = GoogleGenAI(model="gemini-2.0-flash", temperature=0.2)
embed_model = GoogleGenAIEmbedding(model_name="models/embedding-001")

# Configure global settings
Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = 512

# Initialize Pinecone
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pinecone_client.Index("demo2")

# Create a better text splitter
text_splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50,
    paragraph_separator="\n\n"
)

# Load documents only if needed
def calculate_document_hash(url):
    return hashlib.md5(url.encode()).hexdigest()

doc_hash = calculate_document_hash(DATA_URL)
index_exists = False

# Check if vectors exist in Pinecone 
try:
    stats = pinecone_index.describe_index_stats()
    if stats.get("total_vector_count", 0) > 0:
        index_exists = True
        print(f"Found existing index with {stats.get('total_vector_count')} vectors")
except Exception as e:
    print(f"Error checking index: {e}")

# Create vector store and storage context
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

if not index_exists:
    print("Creating new index from documents...")
    # Load documents
    BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
    loader = BeautifulSoupWebReader()
    documents = loader.load_data(urls=[DATA_URL])
    print(f"Loaded {len(documents)} document(s), first document length: {len(documents[0].text)} chars")
    
    # Create index with the text splitter
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context,
        transformations=[text_splitter]
    )
else:
    print("Using existing index...")
    # Use existing index
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# Create a custom QA prompt template
qa_prompt_tmpl = """You are an AI assistant providing helpful answers based on the given context.
Context information is provided below:
---------------------
{context_str}
---------------------

Given this information, please answer the question: {query_str}
If the information is not available in the context, say so - DO NOT make up answers.
Provide a detailed and comprehensive response.
"""

qa_prompt = PromptTemplate(qa_prompt_tmpl)

# Create an advanced retriever and query engine
retriever = index.as_retriever(similarity_top_k=5)
query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    response_mode=ResponseMode.COMPACT,
    verbose=True,
    text_qa_template=qa_prompt,
)

# Run your query
#query = "What does the author think about LlamaIndex?"
query = input("Enter your question: ")

print(f"\nQuerying: '{query}'")
gemini_response = query_engine.query(query)
print("\nResponse:")
print(gemini_response)