select f.airport_in as airport_in, f.airport_out as airport_out, f.time_in as time_in, f.time_out as time_out, s.id, s.date_out, s.date_in
FROM flight f
join schedule s on f.id = s.id_flight
where airport_in = "$airport_in" and airport_out = "$airport_out"