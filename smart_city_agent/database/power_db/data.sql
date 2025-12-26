-- ==========================================
-- Addis-Sync : POWER AGENT SAMPLE DATA
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

-- Power Distribution Offices
INSERT INTO offices (woreda, name, phone, email, location, address) VALUES
('Addis Ketema', 'Addis Ketema Power Distribution Office', '+251-11-557-1234', 'power.addisketema@eepco.gov.et', ST_MakePoint(38.75, 9.02), 'Near Merkato'),
('Arada', 'Arada Power Service Center', '+251-11-557-2345', 'power.arada@eepco.gov.et', ST_MakePoint(38.73, 9.03), 'Arada District'),
('Bole', 'Bole Electricity Office', '+251-11-557-3456', 'power.bole@eepco.gov.et', ST_MakePoint(38.785, 9.00), 'Bole Road'),
('Gullele', 'Gullele Power Distribution', '+251-11-557-4567', 'power.gullele@eepco.gov.et', ST_MakePoint(38.73, 9.06), 'Gullele Area'),
('Kirkos', 'Kirkos Electricity Service', '+251-11-557-5678', 'power.kirkos@eepco.gov.et', ST_MakePoint(38.75, 8.98), 'Kirkos District'),
('Kolfe Keranio', 'Kolfe Power Office', '+251-11-557-6789', 'power.kolfe@eepco.gov.et', ST_MakePoint(38.68, 9.01), 'Kolfe Area'),
('Lideta', 'Lideta Electricity Distribution', '+251-11-557-7890', 'power.lideta@eepco.gov.et', ST_MakePoint(38.71, 8.96), 'Lideta District'),
('Nifas Silk-Lafto', 'Nifas Silk Power Service', '+251-11-557-8901', 'power.nifassilk@eepco.gov.et', ST_MakePoint(38.74, 8.93), 'Nifas Silk Area'),
('Yeka', 'Yeka Power Distribution Office', '+251-11-557-9012', 'power.yeka@eepco.gov.et', ST_MakePoint(38.80, 9.03), 'Yeka Sub-City'),
('Akaki Kality', 'Akaki Electricity Office', '+251-11-557-0123', 'power.akaki@eepco.gov.et', ST_MakePoint(38.80, 8.91), 'Akaki Kality');

-- Sample Power Lines
INSERT INTO power_lines (line_type, voltage_kv, status, geom) VALUES
('transmission_line', 132.00, 'active', ST_GeomFromText('LINESTRING(38.75 9.02, 38.76 9.01)', 4326)),
('distribution_cable', 33.00, 'active', ST_GeomFromText('LINESTRING(38.73 9.03, 38.74 9.02)', 4326)),
('grid_connection', 11.00, 'active', ST_GeomFromText('LINESTRING(38.785 9.00, 38.79 8.99)', 4326));

-- Sample Tickets (for testing)
INSERT INTO tickets (ticket_number, woreda, issue_description, user_contact, status) VALUES
('POWR-TEST001', 'Bole', 'Complete power outage in neighborhood', '+251-900-111111', 'RESOLVED'),
('POWR-TEST002', 'Addis Ketema', 'Transformer making loud noise', '+251-900-222222', 'IN_PROGRESS');
