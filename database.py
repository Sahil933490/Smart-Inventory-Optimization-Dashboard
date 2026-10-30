import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "inventory.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def initialize_database(conn):
    """Create/refresh tables from repository CSVs. Safe to rerun: tables are replaced."""
    inventory = pd.read_csv(ROOT / "data" / "inventory.csv")
    sales = pd.read_csv(ROOT / "data" / "sales.csv")
    optimization = pd.read_csv(ROOT / "data" / "inventory_optimization_results.csv")

    inventory.to_sql("inventory", conn, if_exists="replace", index=False)
    sales.to_sql("sales", conn, if_exists="replace", index=False)
    optimization.to_sql("optimization_results", conn, if_exists="replace", index=False)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(Product_ID)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(Date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_inventory_category ON inventory(Category)")
    conn.commit()
