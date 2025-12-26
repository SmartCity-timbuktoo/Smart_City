-- ==========================================
-- Addis-Sync : INFRASTRUCTURE AGENT SAMPLE DATA
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

-- Infrastructure Offices
INSERT INTO offices (woreda, name, phone, email, location, address) VALUES
('Addis Ketema', 'Addis Ketema Infrastructure Office', '+251-11-777-1234', 'infrastructure.addisketema@aaca.gov.et', ST_MakePoint(38.75, 9.02), 'Near Merkato'),
('Arada', 'Arada Roads & Infrastructure', '+251-11-777-2345', 'infrastructure.arada@aaca.gov.et', ST_MakePoint(38.73, 9.03), 'Arada District'),
('Bole', 'Bole Infrastructure Service', '+251-11-777-3456', 'infrastructure.bole@aaca.gov.et', ST_MakePoint(38.785, 9.00), 'Bole Road'),
('Gullele', 'Gullele Infrastructure Office', '+251-11-777-4567', 'infrastructure.gullele@aaca.gov.et', ST_MakePoint(38.73, 9.06), 'Gullele Area'),
('Kirkos', 'Kirkos Roads & Infrastructure', '+251-11-777-5678', 'infrastructure.kirkos@aaca.gov.et', ST_MakePoint(38.75, 8.98), 'Kirkos District'),
('Kolfe Keranio', 'Kolfe Infrastructure Office', '+251-11-777-6789', 'infrastructure.kolfe@aaca.gov.et', ST_MakePoint(38.68, 9.01), 'Kolfe Area'),
('Lideta', 'Lideta Infrastructure Service', '+251-11-777-7890', 'infrastructure.lideta@aaca.gov.et', ST_MakePoint(38.71, 8.96), 'Lideta District'),
('Nifas Silk-Lafto', 'Nifas Silk Infrastructure', '+251-11-777-8901', 'infrastructure.nifassilk@aaca.gov.et', ST_MakePoint(38.74, 8.93), 'Nifas Silk Area'),
('Yeka', 'Yeka Roads & Infrastructure', '+251-11-777-9012', 'infrastructure.yeka@aaca.gov.et', ST_MakePoint(38.80, 9.03), 'Yeka Sub-City'),
('Akaki Kality', 'Akaki Infrastructure Office', '+251-11-777-0123', 'infrastructure.akaki@aaca.gov.et', ST_MakePoint(38.80, 8.91), 'Akaki Kality');

-- Sample Infrastructure Assets
INSERT INTO infrastructure_assets (asset_type, condition, geom) VALUES
('road', 'good', ST_GeomFromText('LINESTRING(38.75 9.02, 38.76 9.01)', 4326)),
('bridge', 'fair', ST_GeomFromText('LINESTRING(38.73 9.03, 38.74 9.02)', 4326)),
('streetlight', 'good', ST_GeomFromText('LINESTRING(38.785 9.00, 38.79 8.99)', 4326));

-- Sample Tickets (for testing)
INSERT INTO tickets (ticket_number, woreda, issue_description, user_contact, status) VALUES
('INFR-TEST001', 'Bole', 'Large pothole on main road', '+251-900-111111', 'IN_REPAIR'),
('INFR-TEST002', 'Addis Ketema', 'Streetlights not working', '+251-900-222222', 'RESOLVED');
