-- ==========================================
-- Addis-Sync : UTILITY AGENT SAMPLE DATA
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

-- Utility Offices
INSERT INTO offices (woreda, name, phone, email, location, address) VALUES
('Addis Ketema', 'Addis Ketema Utility Office', '+251-11-554-1234', 'utility.addisketema@aawsa.gov.et', ST_MakePoint(38.75, 9.02), 'Near Merkato'),
('Arada', 'Arada Water & Sewerage Office', '+251-11-554-2345', 'utility.arada@aawsa.gov.et', ST_MakePoint(38.73, 9.03), 'Arada District'),
('Bole', 'Bole Utility Service', '+251-11-554-3456', 'utility.bole@aawsa.gov.et', ST_MakePoint(38.785, 9.00), 'Bole Road'),
('Gullele', 'Gullele Utility Office', '+251-11-554-4567', 'utility.gullele@aawsa.gov.et', ST_MakePoint(38.73, 9.06), 'Gullele Area'),
('Kirkos', 'Kirkos Water & Sewerage', '+251-11-554-5678', 'utility.kirkos@aawsa.gov.et', ST_MakePoint(38.75, 8.98), 'Kirkos District'),
('Kolfe Keranio', 'Kolfe Utility Office', '+251-11-554-6789', 'utility.kolfe@aawsa.gov.et', ST_MakePoint(38.68, 9.01), 'Kolfe Area'),
('Lideta', 'Lideta Utility Service', '+251-11-554-7890', 'utility.lideta@aawsa.gov.et', ST_MakePoint(38.71, 8.96), 'Lideta District'),
('Nifas Silk-Lafto', 'Nifas Silk Utility Office', '+251-11-554-8901', 'utility.nifassilk@aawsa.gov.et', ST_MakePoint(38.74, 8.93), 'Nifas Silk Area'),
('Yeka', 'Yeka Water & Sewerage Office', '+251-11-554-9012', 'utility.yeka@aawsa.gov.et', ST_MakePoint(38.80, 9.03), 'Yeka Sub-City'),
('Akaki Kality', 'Akaki Utility Office', '+251-11-554-0123', 'utility.akaki@aawsa.gov.et', ST_MakePoint(38.80, 8.91), 'Akaki Kality');

-- Sample Utility Infrastructure
INSERT INTO utilities (utility_type, pressure_level, status, geom) VALUES
('water_pipe', 3.50, 'operational', ST_GeomFromText('LINESTRING(38.75 9.02, 38.76 9.01)', 4326)),
('sewer_pipe', NULL, 'operational', ST_GeomFromText('LINESTRING(38.73 9.03, 38.74 9.02)', 4326)),
('hydraulic_line', 4.20, 'operational', ST_GeomFromText('LINESTRING(38.785 9.00, 38.79 8.99)', 4326));

-- Sample Tickets (for testing)
INSERT INTO tickets (ticket_number, woreda, issue_description, user_contact, status) VALUES
('UTIL-TEST001', 'Bole', 'Water pipe burst on street', '+251-900-111111', 'RESOLVED'),
('UTIL-TEST002', 'Addis Ketema', 'Low water pressure', '+251-900-222222', 'IN_PROGRESS');
