SELECT 
    v.category_id,
    SUM(vs.view_count) AS total_views
FROM 
    gold.video v
JOIN 
    gold.videostatistics vs 
ON 
    v.statistics_id = vs.stats_id
GROUP BY 
    v.category_id
ORDER BY 
    total_views DESC;