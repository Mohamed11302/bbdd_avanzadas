SELECT
    d.year,
    d.month,
    v.type,
    COUNT(fvs.video_id) AS videos_subidos
FROM
    gold.fact_videostats fvs
JOIN
    gold.dates d ON fvs.date_id = d.date_id
JOIN
    gold.video v ON fvs.video_id = v.video_id
GROUP BY
    d.year,
    d.month,
    v.type
ORDER BY
    d.year DESC,
    d.month DESC,
    v.type;
