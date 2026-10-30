# Smart Inventory Optimization & Demand Analytics

A Streamlit application built with Python, SQLite SQL, Pandas and Plotly.

## Features
- KPI cards: inventory value, product count, reorder-required products and critical products
- Category-wise inventory analysis
- ABC classification
- Monthly and warehouse-wise revenue analysis
- Top products by revenue
- Replenishment list using EOQ, Safety Stock and Reorder Point
- SQL joins, aggregations, CASE statements and parameterized filters

## Dataset
The repository includes synthetic demonstration data:
- 1,000 products
- 10 warehouses
- 365 days of sales in 2025 (365,000 product-day records)

The data is synthetic and is not actual company data.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

The app loads the CSV files into a local SQLite database (`inventory.db`) automatically.
Tables are refreshed from CSV files on app initialization.

## Deploy on Streamlit Community Cloud
1. Upload this project folder to a GitHub repository.
2. Open Streamlit Community Cloud and connect your GitHub account.
3. Select the repository and branch.
4. Set the main file path to `app.py`.
5. Deploy.

Keep `data/` CSV files in the GitHub repository so the deployed app can load them.

## Inventory model assumptions
- Safety Stock = Z × standard deviation of daily demand × √Lead Time (Z = 1.65)
- Reorder Point = average daily demand × lead time + safety stock
- EOQ = √(2 × annual demand × ordering cost / annual holding cost)
- Ordering cost = ₹500 per order; holding rate = 25% of unit cost

These are demonstration assumptions. Validate parameters before using the model for real operational decisions.
