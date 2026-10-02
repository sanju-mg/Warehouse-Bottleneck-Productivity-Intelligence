import os
import pandas as pd
import mysql.connector

# Absolute or relative path to featured dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "data", "processed", "analytics", "dataco_featured.csv")

print(f"Loading dataset from: {CSV_FILE}")
df = pd.read_csv(CSV_FILE)

print(f"Rows to load: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="supply_chain_intelligence"
)

cursor = conn.cursor()

# Safely truncate target table to prevent duplicate records
print("Truncating target table `dataco_fulfillment` prior to load...")
cursor.execute("TRUNCATE TABLE dataco_fulfillment;")
conn.commit()

# Prepare column names and placeholders
columns = ", ".join(f"`{c}`" for c in df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))

sql = f"""
INSERT INTO dataco_fulfillment ({columns})
VALUES ({placeholders})
"""

batch_size = 5000

for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start + batch_size]

    values = [
        tuple(None if pd.isna(v) else v for v in row)
        for row in batch.itertuples(index=False, name=None)
    ]

    cursor.executemany(sql, values)
    conn.commit()

    print(f"Loaded {min(start + batch_size, len(df)):,}/{len(df):,} rows")

# Verify final row count
cursor.execute("SELECT COUNT(*) FROM dataco_fulfillment;")
final_rows = cursor.fetchone()[0]
print(f"Final loaded row count in `dataco_fulfillment`: {final_rows:,}")

cursor.close()
conn.close()

print("MYSQL LOAD COMPLETED SUCCESSFULLY")