SELECT 
    DATEADD(MINUTE, 
            (DATEDIFF(MINUTE, 0, [Timestamp]) / 15) * 15, 
            0) AS TimeBucket,
    --COUNT(*) AS RecordCount,
    AVG([Temperature]) AS AvgTemperature,
    MIN([Temperature]) AS MinTemperature,
    MAX([Temperature]) AS MaxTemperature
FROM [dbo].[WeatherData]
WHERE [Timestamp] > '2026-01-01'
GROUP BY DATEADD(MINUTE, 
                 (DATEDIFF(MINUTE, 0, [Timestamp]) / 15) * 15, 
                 0)
ORDER BY TimeBucket DESC;
