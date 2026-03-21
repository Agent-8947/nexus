import json
import os
import sys
try:
    from neo4j import GraphDatabase
except ImportError:
    print('[ERROR] neo4j package not installed. Run: pip install neo4j')
    sys.exit(1)

URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'nexus_graph_db')
JSON_PATH = os.path.join(os.path.dirname(__file__), '..', 'SYSTEM', 'ARCHIVE_MAP.json')

def run_cypher(tx, query, parameters=None):
    result = tx.run(query, parameters)
    return [record for record in result]

def populate_graph():
    if not os.path.exists(JSON_PATH):
        print(f'[ERROR] {JSON_PATH} not found. Run ARCHIVIST.py first.')
        sys.exit(1)
        
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        archive_map = json.load(f)

    print('[NEXUS Graph] Connecting to DB...')
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()
    except Exception as e:
        print(f'[ERROR] Connection failed: {e}')
        sys.exit(1)

    print('[NEXUS Graph] Connection OK. Wiping old data...')
    with driver.session() as session:
        session.execute_write(run_cypher, 'MATCH (n) DETACH DELETE n')
        session.execute_write(run_cypher, "CREATE (p:Project {name: $name, id: 'CoreIDE'})", parameters={'name': 'IDE_NEXUS'})
        
        print(f'[NEXUS Graph] Ingesting namespaces...')
        for rel_path, items in archive_map.items():
            dir_name = 'ROOT' if rel_path == '.' else rel_path.replace('\\', '/')
            session.execute_write(
                run_cypher, 
                "MATCH (p:Project {id: 'CoreIDE'}) "
                "MERGE (d:Directory {path: $path}) "
                "MERGE (p)-[:CONTAINS]->(d)", 
                parameters={'path': dir_name}
            )
            for f in items.get('files', []):
                session.execute_write(
                    run_cypher, 
                    "MATCH (d:Directory {path: $dir_path}) "
                    "CREATE (f:File {name: $filename}) "
                    "CREATE (d)-[:HAS_FILE]->(f)",
                    parameters={'dir_path': dir_name, 'filename': f}
                )

        res = session.execute_read(run_cypher, 'MATCH (f:File) RETURN count(f) as count')
        res_dir = session.execute_read(run_cypher, 'MATCH (d:Directory) RETURN count(d) as count')
        sample = session.execute_read(run_cypher, 'MATCH (d:Directory)-[:HAS_FILE]->(f:File) RETURN d.path AS dir, f.name AS file LIMIT 3')
        
        print('\n' + '='*55)
        print('✅ NEXUS GRAPH MEMORY TEST COMPLETE')
        print('='*55)
        print(f'Entities in Graph: {res_dir[0]["count"]} Directories, {res[0]["count"]} Files')
        print('Sample connections:')
        for record in sample:
            print(f"  [Directory] {record['dir']} -> [File] {record['file']}")
        print('='*55)
        print('Status: Exit Code 0. The Database is operational and populated.')
        
    driver.close()
    
if __name__ == '__main__':
    populate_graph()
