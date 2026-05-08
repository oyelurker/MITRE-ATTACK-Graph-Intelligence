import os
import sys
import json
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# 1. Load keys
load_dotenv()

# Check for environment variables
required_vars = ["NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD", "OPENAI_API_KEY"]
missing_vars = [var for var in required_vars if not os.environ.get(var)]
if missing_vars:
    print(f"❌ Error: Missing environment variables: {', '.join(missing_vars)}")
    print("Please check your .env file.")
    sys.exit(1)

# 2. Connect to Database
print(f"🔌 Connecting to: {os.environ['NEO4J_URI']}")
try:
    graph = Neo4jGraph(
        url=os.environ["NEO4J_URI"],
        username=os.environ["NEO4J_USERNAME"],
        password=os.environ["NEO4J_PASSWORD"],
    )
    # graph.refresh_schema()
    print("✅ SUCCESS: Connected to Neo4j Cloud!")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    sys.exit(1)

# 3. Setup LLM
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# 4. Define Extraction Logic
kg_prompt = PromptTemplate.from_template("""
Extract entities and relationships from the text.
Text: {text}

Return output strictly in this JSON format:
{{
  "entities": [{{"name": "...", "type": "..."}}],
  "relationships": [{{"source": "...", "relation": "...", "target": "..."}}]
}}
""")

def extract_and_store(text):
    print("⏳ Extracting knowledge from text...")
    try:
        response = llm.invoke(kg_prompt.format(text=text))
        content = response.content.replace("```json", "").replace("```", "").strip()
        kg = json.loads(content)

        # Store Entities
        for entity in kg.get("entities", []):
            graph.query(
                "MERGE (e:Entity {name: $name}) SET e.type = $type",
                {"name": entity["name"], "type": entity["type"]}
            )
        
        # Store Relationships
        for rel in kg.get("relationships", []):
            graph.query(
                """
                MATCH (a:Entity {name: $source})
                MATCH (b:Entity {name: $target})
                MERGE (a)-[r:RELATION {type: $relation}]->(b)
                """,
                {"source": rel["source"], "target": rel["target"], "relation": rel["relation"]}
            )
        print("✅ Knowledge stored!")
    except Exception as e:
        print(f"❌ Error during extraction: {e}")

# 5. Define Retrieval Logic
def graphrag_answer(question):
    print(f"🤔 Thinking about: {question}")
    
    # Logic: Check if the QUESTION contains the ENTITY NAME
    cypher_query = f"""
    MATCH (e:Entity)-[r]->(n)
    WHERE toLower('{question}') CONTAINS toLower(e.name) 
       OR toLower('{question}') CONTAINS toLower(n.name)
    RETURN e.name AS source, r.type AS relation, n.name AS target
    LIMIT 20
    """
    try:
        results = graph.query(cypher_query)
    except Exception as e:
        return f"Error querying graph: {e}"
    
    if not results:
        return "I couldn't find any relevant info in the graph."

    # Build context
    context = "\n".join([f"{row['source']} --{row['relation']}--> {row['target']}" for row in results])
    
    # Generate Answer
    answer_prompt = PromptTemplate.from_template("""
    Graph context: {context}
    Question: {question}
    Answer strictly using the graph context.
    """)
    
    response = llm.invoke(answer_prompt.format(context=context, question=question))
    return response.content

# --- RUN ---
def main():
    print("\n--- GraphRAG Demo ---")
    print("1. Extract Knowledge")
    print("2. Ask Question")
    print("3. Exit")
    
    # Initial data ingestion (Optional, could be made dynamic)
    text_data = """
    Neo4j is a graph database used by enterprises.
    LangChain integrates Neo4j for GraphRAG applications.
    GraphRAG improves multi-hop reasoning in LLMs.
    """
    
    while True:
        choice = input("\nSelect an option (1/2/3) or type 'exit': ").strip().lower()
        
        if choice == '1':
            print(f"\nProcessing default text data:\n{text_data.strip()}\n")
            extract_and_store(text_data)
        elif choice == '2':
            question = input("\n💬 Ask a question: ").strip()
            if question:
                answer = graphrag_answer(question)
                print(f"\n💡 ANSWER: {answer}")
        elif choice == '3' or choice == 'exit':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()