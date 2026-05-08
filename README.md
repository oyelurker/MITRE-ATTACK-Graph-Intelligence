# 🕸️ Simple GraphRAG with Neo4j & LangChain

A proof-of-concept implementation of **Graph Retrieval-Augmented Generation (GraphRAG)**. Unlike traditional Vector RAG, this system builds a Knowledge Graph to understand *relationships* between entities for more accurate, grounded answers.

This version is configured to support both **Google Gemini**(preffered) and **OpenAI** models for entity extraction and generation.

---

## 🚀 Features
* **Knowledge Graph Construction:** Extracts entities and relationships from unstructured text using LLMs.
* **Graph Storage:** Stores structured data natively in **Neo4j**.
* **Graph Retrieval:** Uses Cypher queries to fetch relevant subgraphs for reasoning.
* **Tech Stack:** Python, LangChain, Neo4j, Google Gemini / OpenAI.

---

## 🛠️ Prerequisites
Before running the project, ensure you have:
1. **Python 3.10+**
2. **Neo4j Desktop**
   - Install and create a Local DBMS
   - Set a password (needed for `.env`)
   - Click **Start** before running the project
3. **API Keys**
   - Google Gemini API key OR OpenAI API key

---

## 📦 Installation & Setup Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/oyelurker/GraphRAG-Neo4j-LangChain
cd GraphRAG-Neo4j-LangChain
```

### Step 2: Set Up Virtual Environment (Highly Recommended)
Creating a virtual environment ensures dependencies don’t conflict with other projects.

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create `.env` file:
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env`:
```env
# Neo4j Local Configuration (Using Bolt)
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_local_db_password_here

# API Keys
GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Neo4j Aura (Optional)
# NEO4J_URI=neo4j+s://your_aura_instance.databases.neo4j.io
# NEO4J_USERNAME=your_aura_username_here
# NEO4J_PASSWORD=your_aura_password_here
```

## 🚀 How to Run
Make sure:
- Neo4j is running on port `7687`
- Virtual environment is activated

Run:
```bash
python graphrag.py
```

---

## 🧠 How It Works
1. **Ingestion:** Reads raw text documents  
2. **Extraction:** LLM identifies entities (nodes) and relationships (edges)  
3. **Storage:** Data stored in Neo4j  
4. **Retrieval:** LangChain queries graph  
5. **Answer:** LLM generates grounded response  

---

## 📚 Reference
* **[GraphRAG Explained: Building Knowledge-Grounded LLM Systems with Neo4j and LangChain](https://pub.towardsai.net/graphrag-explained-building-knowledge-grounded-llm-systems-with-neo4j-and-langchain-017a1820763e).