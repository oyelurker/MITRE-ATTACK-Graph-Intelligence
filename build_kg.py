import os
import pandas as pd
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Setup Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_llm_extraction(row_data):
    """Pass row data to Gemini and get structured JSON."""
    prompt = f"""
    Act as a cybersecurity expert. Extract entities from the following MITRE ATT&CK data.
    Data: {row_data}
    
    Return a strict JSON object with the following format:
    {{
        "APT_Group": "Name of the group",
        "Tactic": "Name of the tactic",
        "Software": "Name of the software used"
    }}
    Ensure the output is ONLY the JSON object.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean potential markdown formatting
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error extracting from Gemini: {e}")
        return None

def build_knowledge_graph():
    # 1. Read datasets
    print("Reading datasets...")
    attack_df = pd.read_excel('attackmitre.xlsx')
    enterprise_df = pd.read_excel('MitreEnterprise.xlsx')

    # 2. Prepare for merge
    print("Processing and merging data...")
    attack_df['Tactic ID'] = attack_df['Group Techniques'].str.split('; ')
    attack_exploded = attack_df.explode('Tactic ID')
    attack_exploded['Tactic ID'] = attack_exploded['Tactic ID'].str.strip()

    # Merge
    merged_df = pd.merge(
        attack_exploded, 
        enterprise_df, 
        on='Tactic ID', 
        how='inner'
    )

    # 3. Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        # Clear existing data
        session.run("MATCH (n) DETACH DELETE n")
        
        print(f"Iterating through {len(merged_df)} merged records...")
        processed_count = 0
        for index, row in merged_df.iterrows():
            if processed_count >= 50: # Limit for demonstration
                break
                
            row_info = {
                "APT_Group": row.get('APT Group Name'),
                "Tactic": row.get('Tactic Name'),
                "Software_ID": row.get('Software ID'),
                "Description": row.get('Description')
            }
            
            extracted = get_llm_extraction(row_info)
            if extracted:
                group = extracted.get('APT_Group')
                tactic = extracted.get('Tactic')
                software = extracted.get('Software')
                
                query = """
                MERGE (g:APT_Group {name: $group})
                MERGE (t:Tactic {name: $tactic})
                MERGE (s:Software {name: $software})
                MERGE (g)-[:USES_TACTIC]->(t)
                MERGE (g)-[:USES_SOFTWARE]->(s)
                """
                session.run(query, group=group, tactic=tactic, software=software)
                print(f"Inserted: {group} -> {tactic}, {software}")
                processed_count += 1

    driver.close()
    print("Knowledge Graph build complete!")

if __name__ == "__main__":
    build_knowledge_graph()
