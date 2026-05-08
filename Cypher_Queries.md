# Cypher Queries for MITRE ATT&CK Knowledge Graph

Use these queries in the Neo4j Browser to visualize and analyze the data.

### 1. Visualize the Generalized Graph
This query retrieves APT groups and their associated Tactics and Software, showing the full structure of the knowledge graph.

```cypher
MATCH (g:APT_Group)-[r1:USES_TACTIC]->(t:Tactic)
MATCH (g)-[r2:USES_SOFTWARE]->(s:Software)
RETURN g, r1, t, r2, s
LIMIT 100
```

### 2. Retrieve List of APT Group IDs
This query retrieves a unique list of all APT group names/IDs stored in the database.

```cypher
MATCH (g:APT_Group)
RETURN DISTINCT g.name AS APT_Group_ID
ORDER BY APT_Group_ID
```

### 3. Count Relationships
To verify the data distribution:

```cypher
MATCH (n)-[r]->(m)
RETURN type(r) AS RelationshipType, count(r) AS Count
```
