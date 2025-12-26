INSERT INTO reports (user_id, description, location, status, citizen_chat_id, admin_id)
VALUES 
('user_401', 'Water outage in sector 5', ST_SetSRID(ST_Point(38.790, 9.020), 4326), 'PENDING', '121314151', '991122334'),
('user_402', 'Sewage backup', ST_SetSRID(ST_Point(38.792, 9.022), 4326), 'PENDING', '131415161', '991122334'),
('user_403', 'Gas leak reported', ST_SetSRID(ST_Point(38.791, 9.021), 4326), 'PENDING', '141516171', '991122334'),
('user_404', 'Low water pressure', ST_SetSRID(ST_Point(38.793, 9.019), 4326), 'PENDING', '151617181', '991122334'),
('user_405', 'Pipe burst near park', ST_SetSRID(ST_Point(38.794, 9.018), 4326), 'PENDING', '161718191', '991122334');
