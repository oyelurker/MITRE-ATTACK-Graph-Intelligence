# MITRE ATT&CK Knowledge Graph Intelligence (DS-GKG)
<img width="1342" height="712" alt="image" src="https://github.com/user-attachments/assets/22374ea1-c711-4a55-a7d6-104b1d5dad67" />
- graph for 20 rows of xl 

## 🎯 Project Aim
The goal of this project is to create a **Domain Specific Generalized Knowledge Graph (DS-GKG)** for MITRE ATT&CK. It leverages Python, Neo4j, and the Google Gemini LLM to extract structured relationships between APT Groups, Tactics, and Software from raw datasets.

## 🛠️ Assignment Overview
This implementation fulfills the requirements for the Semester IV Project:
- **Datasets**: Merges `attackmitre.xlsx` and `MitreEnterprise.xlsx` based on Tactic IDs.
- **LLM Extraction**: Uses `gemini-1.5-flash` to identify and structure entity relationships.
- **Database**: Stores the resulting graph in a Neo4j database for visualization and querying.
- **Status**: Currently configured to process **20 records** for demonstration purposes to preserve API quota and ensure stability.

## 🚀 How to Run

### 1. Prerequisites
- Python 3.10+
- Neo4j Desktop installed and running.
- A Google Gemini API Key.

### 2. Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/oyelurker/MITRE-ATTACK-Graph-Intelligence.git
   cd MITRE-ATTACK-Graph-Intelligence
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   - Create a `.env` file based on `.env.example`.
   - Add your Neo4j password and Google API Key.

### 3. Build the Graph
Run the main script to process data and populate Neo4j:
```bash
python build_kg.py
```

### 4. Visualize
Open your Neo4j Browser and run the queries found in `Cypher_Queries.md` to see the results.

## 📊 Future Work
- Increase the processing limit to cover the full 11,000+ records.
- Implement more complex relationship extraction (e.g., specific mitigation steps).
- Integrate with the `graphrag.py` Q&A system for real-time threat intelligence.

## 📚 Reference
* [MITRE ATT&CK Dataset Knowledge Graph Enhanced RAG](https://ieee-dataport.org/documents/mitre-attack-dataset-knowledge-graph-enhanced-rag-cyber-threat-intelligence)
* Built using Google Gemini and LangChain logic.
