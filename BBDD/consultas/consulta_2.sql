 SELECT 
        channel_name, 
        subscribers, 
        video_title, 
        video_type,
        video_views
    FROM (
        SELECT 
            ch.name AS channel_name, 
            cs.subscribers AS subscribers, 
            v.title AS video_title, 
            v.type AS video_type,
            vs.view_count AS video_views,
            ROW_NUMBER() OVER(PARTITION BY ch.name ORDER BY vs.view_count DESC) as rn
        FROM 
            (SELECT 
                stats_id, 
                subscribers 
             FROM 
                gold.channelstatistics 
             ORDER BY 
                subscribers DESC 
             LIMIT 3) AS top_channels
        JOIN 
            gold.channel ch ON ch.statistics_id = top_channels.stats_id
        JOIN 
            gold.channelstatistics cs ON cs.stats_id = ch.statistics_id
        JOIN 
            gold.fact_videostats fvs ON fvs.channel_id = ch.channel_id
        JOIN 
            gold.video v ON v.video_id = fvs.video_id
        JOIN 
            gold.videostatistics vs ON vs.stats_id = v.statistics_id
    ) subquery
    WHERE rn <= 3
    ORDER BY 
        subscribers DESC, video_views DESC;