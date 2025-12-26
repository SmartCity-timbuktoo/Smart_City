INSERT INTO reports (user_id, description, location, status, citizen_chat_id, admin_id)
VALUES 
('user_001', 'Power outage in neighborhood', ST_SetSRID(ST_Point(38.758, 9.005), 4326), 'PENDING', '123456789', '987654321'),
('user_002', 'Transformer issue near main street', ST_SetSRID(ST_Point(38.762, 9.010), 4326), 'PENDING', '234567890', '987654321'),
('user_003', 'Flickering street lights', ST_SetSRID(ST_Point(38.755, 9.002), 4326), 'PENDING', '345678901', '987654321'),
('user_004', 'Broken power line', ST_SetSRID(ST_Point(38.760, 9.008), 4326), 'PENDING', '456789012', '987654321'),
('user_005', 'Substation maintenance required', ST_SetSRID(ST_Point(38.759, 9.007), 4326), 'PENDING', '567890123', '987654321');
