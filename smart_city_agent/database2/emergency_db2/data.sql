INSERT INTO reports (user_id, description, location, status, citizen_chat_id, admin_id)
VALUES 
('user_201', 'Building fire reported', ST_SetSRID(ST_Point(38.770, 9.011), 4326), 'PENDING', '112233445', '991122334'),
('user_202', 'Traffic accident with injuries', ST_SetSRID(ST_Point(38.772, 9.012), 4326), 'PENDING', '223344556', '991122334'),
('user_203', 'Medical emergency: fainted person', ST_SetSRID(ST_Point(38.771, 9.013), 4326), 'PENDING', '334455667', '991122334'),
('user_204', 'Gas leak detected', ST_SetSRID(ST_Point(38.774, 9.010), 4326), 'PENDING', '445566778', '991122334'),
('user_205', 'Collapsed wall reported', ST_SetSRID(ST_Point(38.773, 9.009), 4326), 'PENDING', '556677889', '991122334');
