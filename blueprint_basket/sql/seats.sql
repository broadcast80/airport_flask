select available_seats.id as id, available_seats.number as number, schedule.price as price, flight.airport_in as flight, schedule.id as schedule_id, schedule.date_out as date_out
from available_seats
join schedule on available_seats.id_schedule = schedule.id
join flight on schedule.id_flight = flight.id
where id_schedule = "$id_schedule"
order by number