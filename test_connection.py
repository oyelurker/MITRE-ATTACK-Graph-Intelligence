import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

print(f"🕵️ Testing connection to: {uri}")

try:
    # Attempt 1: Standard Connection
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        print("✅ SUCCESS! Connected securely.")
        
except Exception as e:
    print(f"⚠️ Standard connection failed: {e}")
    print("🔄 Trying fallback (disabling SSL checks)...")
    
    # Attempt 2: Fallback for Strict Networks
    # We change the URI scheme from neo4j+s to bolt+scc manually here
    insecure_uri = uri.replace("neo4j+s://", "bolt+ssc://").replace("neo4j+ssc://", "bolt+ssc://")
    
    try:
        with GraphDatabase.driver(insecure_uri, auth=(user, password)) as driver:
            driver.verify_connectivity()
            print(f"✅ SUCCESS! Connected using fallback URI: {insecure_uri}")
            print("📝 UPDATE YOUR .ENV FILE TO USE THIS URI ABOVE ^")
    except Exception as e2:
        print(f"❌ FAILURE: Could not connect at all. Error: {e2}")