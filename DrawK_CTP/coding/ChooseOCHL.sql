-- 将提供的csv文件名保存为 ag22.csv，生成的OCHL 表格为ochl.csv ----
CREATE TABLE ochl
SELECT YEAR(open.TradingDay) AS year, MONTH(open.TradingDay) AS month, DAY(open.TradingDay) AS day,  open.h, open.m, open.OpenPrice, close.ClosePrice, high.HighPrice, low.LowPrice FROM
(
SELECT TradingDay, HOUR(UpdateTime) AS h, MINUTE(UpdateTime) AS m, LastPrice AS OpenPrice FROM
(SELECT *,ROW_NUMBER() OVER (PARTITION BY TradingDay, HOUR(UPDATETIME), MINUTE(UPDATETIME)) AS seq_num FROM ag22) AS group_table
WHERE seq_num = 1 
GROUP BY TradingDay, UpdateTime, LastPrice
) AS open,

(
SELECT group_table.TradingDay, HOUR(group_table.UpdateTime) AS h,MINUTE(group_table.UpdateTime) AS m, group_table.LastPrice AS ClosePrice FROM 
(SELECT *,ROW_NUMBER() OVER (PARTITION BY TradingDay, HOUR(UpdateTime), MINUTE(UpdateTime)) AS seq_num FROM ag22) AS group_table,
(
SELECT TradingDay, HOUR(UpdateTime) AS close_h, MINUTE(UpdateTime) AS close_m, MAX(seq_num) AS close_seq FROM
(SELECT *,ROW_NUMBER() OVER (PARTITION BY TradingDay, HOUR(UpdateTime), MINUTE(UpdateTime)) AS seq_num FROM ag22) AS group_table
GROUP BY TradingDay, HOUR(UpdateTime), MINUTE(UpdateTime)
) AS max_table
WHERE group_table.TradingDay = max_table.TradingDay 
AND HOUR(group_table.UpdateTime) = max_table.close_h
AND MINUTE(group_table.UpdateTime) = max_table.close_m
AND group_table.seq_num = max_table.close_seq
) AS close,

(
SELECT TradingDay, HOUR(UpdateTime) AS h, MINUTE(UpdateTime) AS m, LastPrice AS HighPrice FROM
(
SELECT *, DENSE_RANK() OVER (PARTITION BY TradingDay, HOUR(UPDATETIME), MINUTE(UPDATETIME) ORDER BY LastPrice DESC) AS r FROM ag22

) AS group_table
WHERE r = 1
GROUP BY TradingDay,HOUR(UpdateTime), MINUTE(UpdateTime), LastPrice
) AS high,

(
SELECT TradingDay, HOUR(UpdateTime) AS h, MINUTE(UpdateTime) AS m, LastPrice AS LowPrice FROM
(
SELECT *, DENSE_RANK() OVER (PARTITION BY TradingDay, HOUR(UPDATETIME), MINUTE(UPDATETIME) ORDER BY LastPrice ASC) AS r FROM ag22

) AS group_table
WHERE r = 1
GROUP BY TradingDay,HOUR(UpdateTime), MINUTE(UpdateTime), LastPrice
) AS low


WHERE open.TradingDay = close.TradingDay 
AND open.h = close.h 
AND open.m = close.m

AND open.TradingDay = high.TradingDay 
AND open.h = high.h 
AND open.m = high.m 

AND open.TradingDay = low.TradingDay 
AND open.h = low.h 
AND open.m = low.m ;




















