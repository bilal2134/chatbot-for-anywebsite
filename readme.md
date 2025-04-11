# 💬 Chatbot for Any Website using Gemini Pro, LlamaIndex & Pinecone

This project is an advanced Retrieval-Augmented Generation (RAG) chatbot built using **Google's Gemini Pro**, **LlamaIndex**, and **Pinecone**. It loads content from any public website, indexes it, and allows users to query the content through a natural language interface.

---

## 🚀 Features

- 🔗 Scrape and parse content from any website URL
- 🧠 Semantic search using vector embeddings (Google GenAI)
- 🏪 Vector storage in Pinecone
- 💡 Intelligent and detailed answers using Gemini Pro
- 📦 Supports persistent storage and reusability of existing vector index
- 🧩 Modular design using LlamaIndex for easy customization

---

## 📂 Project Structure

```
📁 chatbot-website-rag
├── main.py               # Main script for indexing and querying
├── .env                  # Stores API keys
├── requirements.txt      # Python dependencies
└── README.md             # You're reading this!
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/chatbot-website-rag.git
cd chatbot-website-rag
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a `.env` file in the root directory and add your API keys:

```
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

> 🔑 You need access to [Google's GenAI API](https://makersuite.google.com/app) and a [Pinecone](https://www.pinecone.io/start/) account.

### 4. Run the chatbot

```bash
python main.py
```

You will be prompted to enter a question after the indexing or loading process.

---

## 🛠 How It Works

1. **Scraping Content**: Uses `BeautifulSoupWebReader` from LlamaIndex to load and parse a webpage.
2. **Text Chunking**: Splits content into clean semantic chunks using `SentenceSplitter`.
3. **Embedding & Indexing**: Generates vector embeddings using Gemini Pro and stores them in Pinecone.
4. **Query Engine**: Retrieves relevant chunks and generates a detailed answer using a custom prompt and Gemini Pro.

---

## 🧠 Technologies Used

- [Google Gemini Pro (LLM & Embeddings)](https://ai.google.dev/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Pinecone Vector DB](https://www.pinecone.io/)
- Python 3.8+

---

## 📝 Customization

- 🔍 Change `DATA_URL` to scrape a different webpage.
- ⚙️ Adjust `chunk_size`, `chunk_overlap`, or `similarity_top_k` for performance tuning.
- 🗨 Modify `qa_prompt_tmpl` to personalize the tone and structure of responses.

---

## 📈 Use Cases

- Build an FAQ bot for any documentation
- Customer support assistant for product pages
- Internal knowledge base search
- Educational Q&A system

---

## 🙌 Acknowledgements

- Inspired by tutorials and community examples using LlamaIndex + Pinecone + GenAI
- Powered by open-source tools and APIs

---

## 📄 License

MIT License. Feel free to use, share, and contribute.

---
