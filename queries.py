import pandas as pd

def get_kpis(conn, where_sql, params):
    q = f"""
    SELECT
      ROUND(SUM(Current_Stock * Unit_Cost), 2) AS inventory_value,
      COUNT(*) AS products,
      SUM(CASE WHEN Stock_Status='Reorder Required' THEN 1 ELSE 0 END) AS reorder_required,
      SUM(CASE WHEN Risk_Level='Critical' THEN 1 ELSE 0 END) AS critical_products
    FROM optimization_results
    {where_sql}
    """
    row = pd.read_sql_query(q, conn, params=params).iloc[0].fillna(0)
    return {
        "inventory_value": float(row["inventory_value"]),
        "products": int(row["products"]),
        "reorder_required": int(row["reorder_required"]),
        "critical_products": int(row["critical_products"])
    }

def get_category_summary(conn, where_sql, params):
    return pd.read_sql_query(f"""
      SELECT Category, SUM(Current_Stock) AS Stock_Units,
             ROUND(SUM(Current_Stock*Unit_Cost),2) AS Inventory_Value
      FROM optimization_results {where_sql}
      GROUP BY Category ORDER BY Inventory_Value DESC
    """, conn, params=params)

def get_warehouse_revenue(conn, warehouses):
    if not warehouses:
        return pd.DataFrame(columns=["Warehouse","Revenue"])
    marks = ",".join(["?"]*len(warehouses))
    return pd.read_sql_query(f"""
      SELECT Warehouse, ROUND(SUM(Revenue),2) AS Revenue
      FROM sales WHERE Warehouse IN ({marks})
      GROUP BY Warehouse ORDER BY Revenue DESC
    """, conn, params=warehouses)

def get_monthly_revenue(conn, warehouses):
    if not warehouses:
        return pd.DataFrame(columns=["Month","Revenue"])
    marks = ",".join(["?"]*len(warehouses))
    return pd.read_sql_query(f"""
      SELECT substr(Date,1,7) AS Month, ROUND(SUM(Revenue),2) AS Revenue
      FROM sales WHERE Warehouse IN ({marks})
      GROUP BY substr(Date,1,7) ORDER BY Month
    """, conn, params=warehouses)

def get_top_products(conn, warehouses):
    if not warehouses:
        return pd.DataFrame(columns=["Product_ID","Product_Name","Revenue"])
    marks = ",".join(["?"]*len(warehouses))
    return pd.read_sql_query(f"""
      SELECT s.Product_ID, i.Product_Name, ROUND(SUM(s.Revenue),2) AS Revenue
      FROM sales s JOIN inventory i ON s.Product_ID=i.Product_ID
      WHERE s.Warehouse IN ({marks})
      GROUP BY s.Product_ID, i.Product_Name
      ORDER BY Revenue DESC LIMIT 10
    """, conn, params=warehouses)

def get_stock_status(conn, where_sql, params):
    return pd.read_sql_query(f"""
      SELECT Product_ID, Product_Name, Category, Warehouse, Current_Stock,
             ROUND(Average_Daily_Demand,2) AS Avg_Daily_Demand,
             Lead_Time, Safety_Stock, Reorder_Point, Stock_Coverage_Days,
             Stock_Status, Risk_Level, Recommended_Order_Qty, ABC_Category
      FROM optimization_results {where_sql}
      ORDER BY CASE Risk_Level WHEN 'Critical' THEN 1 WHEN 'Warning' THEN 2 ELSE 3 END,
               Stock_Coverage_Days
    """, conn, params=params)

def get_abc_summary(conn, where_sql, params):
    return pd.read_sql_query(f"""
      SELECT ABC_Category, COUNT(*) AS Product_Count
      FROM optimization_results {where_sql}
      GROUP BY ABC_Category ORDER BY ABC_Category
    """, conn, params=params)

def get_reorder_list(conn, where_sql, params):
    return pd.read_sql_query(f"""
      SELECT Product_ID, Product_Name, Category, Warehouse, Current_Stock,
             Reorder_Point, EOQ, Recommended_Order_Qty, Risk_Level
      FROM optimization_results
      {where_sql} AND Stock_Status='Reorder Required'
      ORDER BY CASE Risk_Level WHEN 'Critical' THEN 1 WHEN 'Warning' THEN 2 ELSE 3 END,
               Stock_Coverage_Days
    """, conn, params=params)
