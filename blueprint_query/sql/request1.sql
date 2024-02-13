SELECT *
FROM ticket
WHERE sell_time >= DATE_SUB(CURDATE(), INTERVAL '$date' DAY)
order by sell_time DESC