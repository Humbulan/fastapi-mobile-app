#!/usr/bin/env python3
from db_config import get_db_connection
import sqlite3
import json
import csv
from datetime import datetime

print("🏛️ IMPERIAL NATIVE LDA EXTRACTOR")
print("="*60)

db_path = 'instance/imperial.db'
corpus_path = 'lda_corpus.txt'
metadata_path = 'lda_metadata.json'

try:
    conn = get_db_connection()
    cursor = conn.cursor()

    print("\n📊 EXTRACTING TRANSACTION DATA...")
    query = """
    SELECT 
        amount, payment_method, status,
        CASE 
            WHEN payment_method LIKE 'SADC%' THEN 
                payment_method || ' corridor transaction of R' || printf('%.2f', amount)
            WHEN payment_method IN ('mtn_momo', 'mobile_money') THEN 
                'Mobile money payment of R' || printf('%.2f', amount) || ' via ' || payment_method
            ELSE 
                'Payment of R' || printf('%.2f', amount) || ' using ' || payment_method
        END
    FROM payment 
    WHERE status IN ('completed', 'pending')
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()

    descriptions = []
    total_value = 0
    method_counts = {}
    status_counts = {}

    for row in rows:
        amount, method, status, desc = row
        descriptions.append(desc)
        total_value += amount
        method_counts[method] = method_counts.get(method, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    # Try USSD Data
    try:
        cursor.execute("SELECT session_data FROM ussd_session")
        ussd_rows = cursor.fetchall()
        for u_row in ussd_rows:
            descriptions.append(f"USSD interaction: {u_row[0]}")
    except sqlite3.OperationalError:
        print("  ⚠️ No USSD table found, skipping...")

    # Save Corpus
    with open(corpus_path, 'w') as f:
        for desc in descriptions:
            f.write(f"{desc}\n")

    # Save Metadata
    summary = {
        'total_records': len(descriptions),
        'total_value': total_value,
        'by_method': method_counts,
        'by_status': status_counts,
        'timestamp': datetime.now().isoformat()
    }
    with open(metadata_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Extracted {len(descriptions)} records")
    print(f"📁 Corpus: {corpus_path}")
    print(f"📊 Total Value: R{total_value:,.2f}")

    conn.close()
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n✅ Extraction complete")
