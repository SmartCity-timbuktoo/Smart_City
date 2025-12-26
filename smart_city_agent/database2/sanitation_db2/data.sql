INSERT INTO reports (user_id, description, location, status, citizen_chat_id, admin_id)
VALUES 
('user_101', 'Garbage overflow in street', ST_SetSRID(ST_Point(38.765, 9.006), 4326), 'PENDING', '223344556', '998877665'),
('user_102', 'Clogged drain near market', ST_SetSRID(ST_Point(38.768, 9.009), 4326), 'PENDING', '334455667', '998877665'),
('user_103', 'Illegal dumping site detected', ST_SetSRID(ST_Point(38.762, 9.004), 4326), 'PENDING', '445566778', '998877665'),
('user_104', 'Overflowing public bins', ST_SetSRID(ST_Point(38.766, 9.007), 4326), 'PENDING', '556677889', '998877665'),
('user_105', 'Blocked sewer manhole', ST_SetSRID(ST_Point(38.769, 9.008), 4326), 'PENDING', '667788990', '998877665');
