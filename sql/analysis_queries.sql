-- ============================================================================
-- AromaKart Perfume Sales Analytics — SQL Analysis Queries
-- Database: perfume_sales.db | Table: perfume_sales
-- Day 3 of 7 — answers the 15 business questions from Day 1
-- ============================================================================

-- Q1. Month-over-month revenue trend (Jan 2025 - Jun 2026)
SELECT
    strftime('%Y-%m', Order_Date) AS order_month,
    ROUND(SUM(Total_Amount), 2)   AS total_revenue,
    COUNT(*)                      AS total_orders
FROM perfume_sales
GROUP BY order_month
ORDER BY order_month;

-- Q2. Top cities by revenue and order volume
SELECT
    City,
    ROUND(SUM(Total_Amount), 2) AS total_revenue,
    COUNT(*)                    AS total_orders,
    ROUND(AVG(Total_Amount), 2) AS avg_order_value
FROM perfume_sales
GROUP BY City
ORDER BY total_revenue DESC;

-- Q3. Top brands/perfumes by revenue vs. by volume
SELECT Brand, ROUND(SUM(Total_Amount), 2) AS total_revenue, COUNT(*) AS total_orders
FROM perfume_sales
GROUP BY Brand
ORDER BY total_revenue DESC;

SELECT Brand, Perfume_Name, ROUND(SUM(Total_Amount), 2) AS total_revenue, COUNT(*) AS total_orders
FROM perfume_sales
GROUP BY Brand, Perfume_Name
ORDER BY total_orders DESC
LIMIT 10;

-- Q4. Seasonal spikes: Diwali (Oct-Nov), Valentine's (Feb), New Year (Dec-Jan), Wedding season
SELECT
    CASE
        WHEN strftime('%m', Order_Date) IN ('10','11') THEN 'Diwali Season'
        WHEN strftime('%m', Order_Date) = '02'          THEN 'Valentine''s Season'
        WHEN strftime('%m', Order_Date) IN ('12','01')  THEN 'New Year Season'
        ELSE 'Regular Season'
    END AS season,
    ROUND(SUM(Total_Amount), 2) AS total_revenue,
    COUNT(*)                    AS total_orders,
    ROUND(AVG(Total_Amount), 2) AS avg_order_value
FROM perfume_sales
GROUP BY season
ORDER BY total_revenue DESC;

-- Q5. Revenue share: repeat customers vs. one-time buyers
WITH customer_orders AS (
    SELECT Customer_ID, COUNT(*) AS order_count, SUM(Total_Amount) AS customer_revenue
    FROM perfume_sales
    GROUP BY Customer_ID
)
SELECT
    CASE WHEN order_count > 1 THEN 'Repeat Customer' ELSE 'One-Time Customer' END AS customer_type,
    COUNT(*)                       AS num_customers,
    ROUND(SUM(customer_revenue),2) AS total_revenue,
    ROUND(100.0 * SUM(customer_revenue) / (SELECT SUM(Total_Amount) FROM perfume_sales), 2) AS pct_of_total_revenue
FROM customer_orders
GROUP BY customer_type;

-- Q6. Top 20 customers by lifetime spend
SELECT
    Customer_ID,
    Customer_Name,
    COUNT(*)                    AS total_orders,
    ROUND(SUM(Total_Amount), 2) AS lifetime_spend
FROM perfume_sales
GROUP BY Customer_ID, Customer_Name
ORDER BY lifetime_spend DESC
LIMIT 20;

-- Q7. Average discount per brand tier and its relationship to order volume
SELECT
    CASE
        WHEN Brand IN ('Dior','Chanel','Gucci','Versace','Tom Ford','Burberry','Armani') THEN 'Premium'
        WHEN Brand IN ('Calvin Klein','Zara') THEN 'Mid'
        ELSE 'Budget'
    END AS brand_tier,
    ROUND(AVG(Discount_Percentage), 2) AS avg_discount_pct,
    COUNT(*)                           AS total_orders,
    ROUND(SUM(Total_Amount), 2)        AS total_revenue
FROM perfume_sales
GROUP BY brand_tier
ORDER BY total_orders DESC;

-- Q8. Payment method mix — overall and by city
SELECT Payment_Method, COUNT(*) AS total_orders,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM perfume_sales), 2) AS pct_of_orders
FROM perfume_sales
GROUP BY Payment_Method
ORDER BY total_orders DESC;

SELECT City, Payment_Method, COUNT(*) AS total_orders
FROM perfume_sales
GROUP BY City, Payment_Method
ORDER BY City, total_orders DESC;

-- Q9. Return and cancellation rate overall, and by brand tier
SELECT
    Delivery_Status,
    COUNT(*) AS total_orders,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM perfume_sales), 2) AS pct_of_orders
FROM perfume_sales
GROUP BY Delivery_Status;

SELECT
    CASE
        WHEN Brand IN ('Dior','Chanel','Gucci','Versace','Tom Ford','Burberry','Armani') THEN 'Premium'
        WHEN Brand IN ('Calvin Klein','Zara') THEN 'Mid'
        ELSE 'Budget'
    END AS brand_tier,
    Delivery_Status,
    COUNT(*) AS total_orders
FROM perfume_sales
GROUP BY brand_tier, Delivery_Status
ORDER BY brand_tier, Delivery_Status;

-- Q10. Category performance by city
SELECT City, Category, COUNT(*) AS total_orders, ROUND(SUM(Total_Amount), 2) AS total_revenue
FROM perfume_sales
GROUP BY City, Category
ORDER BY City, total_revenue DESC;

-- Q11. Average order value by city vs. national average
SELECT
    City,
    ROUND(AVG(Total_Amount), 2) AS city_avg_order_value,
    (SELECT ROUND(AVG(Total_Amount), 2) FROM perfume_sales) AS national_avg_order_value
FROM perfume_sales
GROUP BY City
ORDER BY city_avg_order_value DESC;

-- Q12. Monthly discount "cost" (gross revenue lost to discounting) vs. volume
SELECT
    strftime('%Y-%m', Order_Date)                              AS order_month,
    ROUND(SUM(Price * Quantity), 2)                             AS gross_revenue_before_discount,
    ROUND(SUM(Price * Quantity) - SUM(Total_Amount), 2)         AS revenue_lost_to_discount,
    COUNT(*)                                                    AS total_orders
FROM perfume_sales
GROUP BY order_month
ORDER BY order_month;

-- Q13. Cancellation/return rate by payment method
SELECT
    Payment_Method,
    ROUND(100.0 * SUM(CASE WHEN Delivery_Status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN Delivery_Status = 'Returned' THEN 1 ELSE 0 END) / COUNT(*), 2)  AS return_rate_pct,
    COUNT(*) AS total_orders
FROM perfume_sales
GROUP BY Payment_Method
ORDER BY cancellation_rate_pct DESC;

-- Q14. Relationship between order quantity and discount percentage
SELECT
    Quantity,
    ROUND(AVG(Discount_Percentage), 2) AS avg_discount_pct,
    COUNT(*)                           AS total_orders
FROM perfume_sales
GROUP BY Quantity
ORDER BY Quantity;

-- Q15. Revenue-per-order-line efficiency by brand
SELECT
    Brand,
    ROUND(SUM(Total_Amount), 2)               AS total_revenue,
    COUNT(*)                                  AS total_orders,
    ROUND(SUM(Total_Amount) / COUNT(*), 2)    AS revenue_per_order
FROM perfume_sales
GROUP BY Brand
ORDER BY revenue_per_order DESC;
