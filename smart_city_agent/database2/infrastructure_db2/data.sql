INSERT INTO reports (user_id, description, location, status, citizen_chat_id, admin_id)
VALUES 
('user_301', 'Pothole on main road', ST_SetSRID(ST_Point(38.780, 9.015), 4326), 'PENDING', '667788990', '990011223'),
('user_302', 'Broken sidewalk', ST_SetSRID(ST_Point(38.782, 9.016), 4326), 'PENDING', '778899001', '990011223'),
('user_303', 'Damaged bridge handrail', ST_SetSRID(ST_Point(38.783, 9.014), 4326), 'PENDING', '889900112', '990011223'),
('user_304', 'Cracked road near school', ST_SetSRID(ST_Point(38.781, 9.013), 4326), 'PENDING', '990011223', '990011223'),
('user_305', 'Street light pole leaning', ST_SetSRID(ST_Point(38.784, 9.012), 4326), 'PENDING', '101112131', '990011223');
