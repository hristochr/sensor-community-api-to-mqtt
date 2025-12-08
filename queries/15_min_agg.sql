SELECT 
    DATEADD(MINUTE, 
            (DATEDIFF(MINUTE, 0, [Timestamp]) / 15) * 15, 
            0) AS TimeBucket,
    --COUNT(*) AS RecordCount,
    AVG([Temperature]) AS AvgTemperature,
    MIN([Temperature]) AS MinTemperature,
    MAX([Temperature]) AS MaxTemperature
FROM [dbo].[WeatherData]
WHERE [Timestamp] > '2025-10-26'
GROUP BY DATEADD(MINUTE, 
                 (DATEDIFF(MINUTE, 0, [Timestamp]) / 15) * 15, 
                 0)
ORDER BY TimeBucket DESC;
