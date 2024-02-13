select airport_in, airport_out, ticket_price, ticket_count, flight_count, money, flight_date from report1
where flight_date >= '$start' and flight_date <= '$end';