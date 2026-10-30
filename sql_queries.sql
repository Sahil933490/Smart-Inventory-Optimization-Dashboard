-- 1. Preview inventory
SELECT * FROM inventory LIMIT 10;

-- 2. Low-stock products
SELECT Product_ID, Product_Name, Current_Stock, Reorder_Point, Risk_Level
FROM optimization_results
WHERE Stock_Status = 'Reorder Required'
ORDER BY Stock_Coverage_Days;

-- 3. Category-wise inventory value
SELECT Category,
       SUM(Current_Stock) AS Total_Stock,
       ROUND(SUM(Current_Stock * Unit_Cost), 2) AS Inventory_Value
FROM inventory
GROUP BY Category
ORDER BY Inventory_Value DESC;

-- 4. Warehouse-wise revenue
SELECT Warehouse, ROUND(SUM(Revenue), 2) AS Total_Revenue
FROM sales
GROUP BY Warehouse
ORDER BY Total_Revenue DESC;

-- 5. Product revenue using JOIN
SELECT i.Product_ID, i.Product_Name,
       ROUND(SUM(s.Revenue), 2) AS Total_Revenue
FROM inventory i
JOIN sales s ON i.Product_ID = s.Product_ID
GROUP BY i.Product_ID, i.Product_Name
ORDER BY Total_Revenue DESC
LIMIT 10;

-- 6. Monthly revenue
SELECT substr(Date, 1, 7) AS Month,
       ROUND(SUM(Revenue), 2) AS Monthly_Revenue
FROM sales
GROUP BY substr(Date, 1, 7)
ORDER BY Month;

-- 7. ABC analysis summary
SELECT ABC_Category, COUNT(*) AS Product_Count,
       ROUND(SUM(Annual_Consumption_Value), 2) AS Consumption_Value
FROM optimization_results
GROUP BY ABC_Category
ORDER BY ABC_Category;

-- 8. Window function: rank products by revenue
WITH product_revenue AS (
    SELECT Product_ID, SUM(Revenue) AS Total_Revenue
    FROM sales
    GROUP BY Product_ID
)
SELECT Product_ID, ROUND(Total_Revenue, 2) AS Total_Revenue,
       RANK() OVER (ORDER BY Total_Revenue DESC) AS Revenue_Rank
FROM product_revenue
ORDER BY Revenue_Rank
LIMIT 20;
