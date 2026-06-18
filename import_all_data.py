from db_config import get_db_connection
import sqlite3
import os
from datetime import datetime

def connect_db(path):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        return conn
    except:
        return None

def import_from_community_nexus():
    print("\n📡 Importing from Community Nexus...")
    nexus_path = os.path.expanduser("~/humbu_community_nexus/community_nexus.db")
    if not os.path.exists(nexus_path):
        print("  ❌ community_nexus.db not found")
        return
    
    nexus = connect_db(nexus_path)
    if not nexus:
        print("  ❌ Could not connect to community_nexus.db")
        return
    
    # Connect to imperial db
    imperial = connect_db("instance/imperial.db")
    
    # Get all tables from nexus
    tables = nexus.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    
    for table in tables:
        table_name = table['name']
        print(f"  📋 Processing table: {table_name}")
        
        try:
            # Get column info
            columns = nexus.execute(f"PRAGMA table_info({table_name});").fetchall()
            col_names = [col['name'] for col in columns]
            
            # Get data
            data = nexus.execute(f"SELECT * FROM {table_name} LIMIT 10;").fetchall()
            
            if data:
                print(f"    Found {len(data)} records")
                for row in data:
                    print(f"    Sample: {dict(row)}")
                    
                    # Here we can add logic to map this data to our imperial schema
                    # For now, we'll create a backup table in imperial
                    
                    # Create a table in imperial to store this data
                    imperial.execute(f"""
                        CREATE TABLE IF NOT EXISTS nexus_backup_{table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            {', '.join([f'"{col}" TEXT' for col in col_names if col != 'id'])},
                            imported_at TIMESTAMP
                        )
                    """)
                    
                    # Insert data
                    for row in data:
                        placeholders = ','.join(['?' for _ in col_names if _ != 'id'])
                        cols = [c for c in col_names if c != 'id']
                        values = [str(row[c]) for c in cols]
                        values.append(datetime.now())
                        
                        imperial.execute(f"""
                            INSERT OR IGNORE INTO nexus_backup_{table_name} 
                            ({', '.join([f'"{c}"' for c in cols])}, imported_at)
                            VALUES ({placeholders}, ?)
                        """, values)
                    
                    imperial.commit()
                    print(f"    ✅ Imported to imperial.nexus_backup_{table_name}")
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    nexus.close()
    imperial.close()

def import_from_vault():
    print("\n🔐 Importing from Vault...")
    vault_path = os.path.expanduser("~/humbu_community_nexus/vault.db")
    if not os.path.exists(vault_path):
        print("  ❌ vault.db not found")
        return
    
    vault = connect_db(vault_path)
    if not vault:
        print("  ❌ Could not connect to vault.db")
        return
    
    imperial = connect_db("instance/imperial.db")
    
    # Check for API keys or secrets
    tables = vault.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    
    for table in tables:
        table_name = table['name']
        print(f"  📋 Processing vault table: {table_name}")
        
        try:
            data = vault.execute(f"SELECT * FROM {table_name} LIMIT 5;").fetchall()
            if data:
                print(f"    Found {len(data)} records")
                for row in data:
                    print(f"    Vault entry: {dict(row)}")
                    
                    # If this contains API keys, import them
                    if 'key' in row.keys() or 'api_key' in row.keys():
                        # Logic to import API keys
                        pass
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    vault.close()
    imperial.close()

if __name__ == "__main__":
    print("="*50)
    print("IMPERIAL DATA IMPORT TOOL")
    print("="*50)
    
    import_from_community_nexus()
    import_from_vault()
    
    print("\n✅ Import complete! Check instance/imperial.db for nexus_backup_* tables")
