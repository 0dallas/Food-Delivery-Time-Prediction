## Additional Business-Related Analyses
### 1. Efficiency Climate Impact Analysis

**Business value: Allows adjusting expectations and resources according to climate**

```sql
-- How does climate affect different areas and types of cooking?
SELECT 
    r.area AS restaurant_area,
    r.cuisine_type,
    d.weather_condition,
    ROUND(AVG(d.delivery_time_min), 2) AS avg_delivery_time,
    ROUND(AVG(d.delivery_rating), 2) AS avg_rating,
    COUNT(*) AS total_deliveries,
    ROUND(AVG(o.order_value), 2) AS avg_order_value
FROM deliveries d
JOIN orders o ON d.delivery_id = o.delivery_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE d.order_placed_at >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY r.area, r.cuisine_type, d.weather_condition
HAVING COUNT(*) >= 20  -- Suficientes datos
ORDER BY r.area, r.cuisine_type, avg_delivery_time DESC;
```

### 2. Identification of Peak Schedules and Staff Optimization

**Business value: Optimize work schedules and anticipate demand**

```sql
-- Analysis of time patterns by weekday
SELECT 
    EXTRACT(DOW FROM d.order_placed_at) AS day_of_week,
    CASE EXTRACT(DOW FROM d.order_placed_at)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday' 
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_name,
    EXTRACT(HOUR FROM d.order_placed_at) AS hour_of_day,
    COUNT(*) AS order_count,
    ROUND(AVG(d.delivery_time_min), 2) AS avg_delivery_time,
    ROUND(AVG(d.delivery_rating), 2) AS avg_rating,
    COUNT(DISTINCT d.delivery_person_id) AS active_delivery_people
FROM deliveries d
WHERE d.order_placed_at >= CURRENT_DATE - INTERVAL '2 months'
GROUP BY 
    EXTRACT(DOW FROM d.order_placed_at),
    EXTRACT(HOUR FROM d.order_placed_at)
ORDER BY day_of_week, hour_of_day;
```

### 3. Profitability Analysis by Distance and Time

**Business value: Identify the most profitable zones and types of cooking**

```sql
-- Which deliveries are most profitable considering distance and time?
SELECT 
    EXTRACT(DOW FROM d.order_placed_at) AS day_of_week,
    CASE EXTRACT(DOW FROM d.order_placed_at)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday' 
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_name,
    EXTRACT(HOUR FROM d.order_placed_at) AS hour_of_day,
    COUNT(*) AS order_count,
    ROUND(AVG(d.delivery_time_min), 2) AS avg_delivery_time,
    ROUND(AVG(d.delivery_rating), 2) AS avg_rating,
    COUNT(DISTINCT d.delivery_person_id) AS active_delivery_people
FROM deliveries d
WHERE d.order_placed_at >= CURRENT_DATE - INTERVAL '2 months'
GROUP BY 
    EXTRACT(DOW FROM d.order_placed_at),
    EXTRACT(HOUR FROM d.order_placed_at)
ORDER BY day_of_week, hour_of_day;
```