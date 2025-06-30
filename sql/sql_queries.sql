-- Question number: 1 "Top 5 customer areas with highest average delivery time in the last 30 days."
SELECT 
    customer_area, 
    AVG(delivery_time_min) AS avg_delivery_time_min,
    COUNT(*) AS total_deliveries,
FROM deliveries
WHERE order_placed_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY customer_area
ORDER BY avg_delivery_time_min DESC
LIMIT 5;

-- Question number: 2 "Average delivery time per traffic condition, by restaurant area and cuisine type."
SELECT 
    r.area AS restaurant_area,
    r.cuisine_type,
    d.traffic_condition,
    AVG(d.delivery_time_min) AS avg_delivery_time_min,
    COUNT(*) AS delivery_count
FROM deliveries d
JOIN orders o ON d.delivery_id = o.delivery_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.area, r.cuisine_type, d.traffic_condition
ORDER BY r.area, r.cuisine_type, d.traffic_condition;

-- Question number: 3 "Top 10 delivery people with the fastest average delivery time, considering only those with at least 50 deliveries and who are still active."
SELECT 
    dp.delivery_person_id,
    dp.name,
    dp.region,
    AVG(d.delivery_time_min) AS avg_delivery_time_min,
    COUNT(*) AS total_deliveries
FROM deliveries d
JOIN delivery_persons dp ON d.delivery_person_id::INT = dp.delivery_person_id
WHERE dp.is_active = true
GROUP BY dp.delivery_person_id, dp.name, dp.region
HAVING COUNT(*) >= 50
ORDER BY avg_delivery_time_min ASC
LIMIT 10;

-- Question number: 4 "The most profitable restaurant area in the last 3 months, defined as the area with the highest total order value."
SELECT 
    r.area,
    SUM(o.order_value) AS total_order_value,
    COUNT(DISTINCT o.order_id) AS total_orders,
    AVG(o.order_value) AS avg_order_value
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN deliveries d ON o.delivery_id = d.delivery_id
WHERE d.order_placed_at >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY r.area
ORDER BY total_order_value DESC
LIMIT 1;

-- Question number: 5 "Identify whether any delivery people show an increasing trend in average delivery time."
-- This query identifies delivery people showing an increasing trend in average delivery time.
-- It uses two time windows:
-- Recent period: Last month
-- Reference period: Month that occurred 3-4 months ago
WITH performance_comparison AS (
    SELECT 
        dp.delivery_person_id,
        dp.name,
        AVG(CASE 
            WHEN d.order_placed_at >= CURRENT_DATE - INTERVAL '1 month' 
            THEN d.delivery_time_min 
        END) AS recent_avg_time,
        AVG(CASE 
            WHEN d.order_placed_at >= CURRENT_DATE - INTERVAL '4 months' 
                AND d.order_placed_at < CURRENT_DATE - INTERVAL '3 months'
            THEN d.delivery_time_min 
        END) AS older_avg_time,
        COUNT(CASE 
            WHEN d.order_placed_at >= CURRENT_DATE - INTERVAL '1 month' 
            THEN 1 
        END) AS recent_deliveries,
        COUNT(CASE 
            WHEN d.order_placed_at >= CURRENT_DATE - INTERVAL '4 months' 
                AND d.order_placed_at < CURRENT_DATE - INTERVAL '3 months'
            THEN 1 
        END) AS older_deliveries
    FROM deliveries d
    JOIN delivery_persons dp ON d.delivery_person_id::INT = dp.delivery_person_id
    WHERE dp.is_active = true
        AND d.order_placed_at >= CURRENT_DATE - INTERVAL '4 months'
    GROUP BY dp.delivery_person_id, dp.name
)
SELECT 
    delivery_person_id,
    name,
    ROUND(recent_avg_time, 2) AS recent_month_avg_time,
    ROUND(older_avg_time, 2) AS three_months_ago_avg_time,
    ROUND(recent_avg_time - older_avg_time, 2) AS time_increase,
    recent_deliveries,
    older_deliveries
FROM performance_comparison
WHERE recent_avg_time IS NOT NULL 
    AND older_avg_time IS NOT NULL
    AND recent_deliveries >= 15  -- Minimum deliveries for reliable comparison
    AND older_deliveries >= 15
    AND recent_avg_time > older_avg_time  -- Only show those with increasing times
ORDER BY (recent_avg_time - older_avg_time) DESC;