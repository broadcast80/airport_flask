SELECT f.airport_in as airport_in, f.airport_out as airport_out, f.time_in as time_in, s.date_out as date_out, s.price as price, s.id as id
FROM flight f
join schedule s on f.id = s.id_flight
ORDER BY s.date_out