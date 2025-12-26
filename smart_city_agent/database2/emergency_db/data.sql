-- ==========================================
-- Addis-Sync : EMERGENCY AGENT SAMPLE DATA
-- ==========================================

-- Woredas (Major Addis Ababa Sub-Cities)
INSERT INTO woredas (name, geom) VALUES
('Addis Ketema', ST_GeomFromText('POLYGON((38.74 9.01,38.76 9.01,38.76 9.03,38.74 9.03,38.74 9.01))',4326)),
('Arada', ST_GeomFromText('POLYGON((38.72 9.02,38.74 9.02,38.74 9.04,38.72 9.04,38.72 9.02))',4326)),
('Bole', ST_GeomFromText('POLYGON((38.77 8.99,38.80 8.99,38.80 9.01,38.77 9.01,38.77 8.99))',4326)),
('Gullele', ST_GeomFromText('POLYGON((38.72 9.05,38.74 9.05,38.74 9.07,38.72 9.07,38.72 9.05))',4326)),
('Kirkos', ST_GeomFromText('POLYGON((38.74 8.97,38.76 8.97,38.76 8.99,38.74 8.99,38.74 8.97))',4326)),
('Kolfe Keranio', ST_GeomFromText('POLYGON((38.67 9.00,38.69 9.00,38.69 9.02,38.67 9.02,38.67 9.00))',4326)),
('Lideta', ST_GeomFromText('POLYGON((38.70 8.95,38.72 8.95,38.72 8.97,38.70 8.97,38.70 8.95))',4326)),
('Nifas Silk-Lafto', ST_GeomFromText('POLYGON((38.73 8.92,38.75 8.92,38.75 8.94,38.73 8.94,38.73 8.92))',4326)),
('Yeka', ST_GeomFromText('POLYGON((38.79 9.02,38.81 9.02,38.81 9.04,38.79 9.04,38.79 9.02))',4326)),
('Akaki Kality', ST_GeomFromText('POLYGON((38.79 8.90,38.81 8.90,38.81 8.92,38.79 8.92,38.79 8.90))',4326));

-- Emergency Offices
INSERT INTO offices (woreda, name, phone, email, location, address) VALUES
('Addis Ketema', 'Addis Ketema Emergency Response Center', '+251-11-888-1234', 'emergency.addisketema@aa.gov.et', ST_MakePoint(38.75, 9.02), 'Near Piazza'),
('Arada', 'Arada Fire & Emergency Station', '+251-11-888-2345', 'emergency.arada@aa.gov.et', ST_MakePoint(38.73, 9.03), 'Near Merkato'),
('Bole', 'Bole Emergency Services', '+251-11-888-3456', 'emergency.bole@aa.gov.et', ST_MakePoint(38.785, 9.00), 'Bole Road'),
('Gullele', 'Gullele Emergency Response Unit', '+251-11-888-4567', 'emergency.gullele@aa.gov.et', ST_MakePoint(38.73, 9.06), 'Gullele Area'),
('Kirkos', 'Kirkos Emergency Center', '+251-11-888-5678', 'emergency.kirkos@aa.gov.et', ST_MakePoint(38.75, 8.98), 'Kirkos District'),
('Kolfe Keranio', 'Kolfe Emergency Station', '+251-11-888-6789', 'emergency.kolfe@aa.gov.et', ST_MakePoint(38.68, 9.01), 'Kolfe Area'),
('Lideta', 'Lideta Fire & Rescue', '+251-11-888-7890', 'emergency.lideta@aa.gov.et', ST_MakePoint(38.71, 8.96), 'Lideta District'),
('Nifas Silk-Lafto', 'Nifas Silk Emergency Services', '+251-11-888-8901', 'emergency.nifassilk@aa.gov.et', ST_MakePoint(38.74, 8.93), 'Nifas Silk Area'),
('Yeka', 'Yeka Emergency Response', '+251-11-888-9012', 'emergency.yeka@aa.gov.et', ST_MakePoint(38.80, 9.03), 'Yeka Sub-City'),
('Akaki Kality', 'Akaki Emergency Station', '+251-11-888-0123', 'emergency.akaki@aa.gov.et', ST_MakePoint(38.80, 8.91), 'Akaki Kality');

-- Sample Emergency Routes
INSERT INTO emergency_routes (route_type, priority_level, geom) VALUES
('fire_route', 1, ST_GeomFromText('LINESTRING(38.75 9.02, 38.76 9.01)', 4326)),
('ambulance_path', 1, ST_GeomFromText('LINESTRING(38.73 9.03, 38.74 9.02)', 4326)),
('evacuation_route', 2, ST_GeomFromText('LINESTRING(38.785 9.00, 38.79 8.99)', 4326));

-- Sample Tickets (for testing)
INSERT INTO tickets (ticket_number, woreda, emergency_type, issue_description, user_contact, status) VALUES
('EMER-TEST001', 'Bole', 'fire', 'Building fire reported', '+251-900-111111', 'RESOLVED'),
('EMER-TEST002', 'Addis Ketema', 'medical', 'Medical emergency at Piazza', '+251-900-222222', 'CLOSED');
