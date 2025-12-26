-- ==========================================
-- Addis-Sync : SANITATION AGENT SAMPLE DATA
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

-- Sanitation Offices
INSERT INTO offices (woreda, name, phone, email, location, address) VALUES
('Addis Ketema', 'Addis Ketema Sanitation Office', '+251-11-665-1234', 'sanitation.addisketema@aaca.gov.et', ST_MakePoint(38.75, 9.02), 'Near Merkato'),
('Arada', 'Arada Waste Management Center', '+251-11-665-2345', 'sanitation.arada@aaca.gov.et', ST_MakePoint(38.73, 9.03), 'Arada District'),
('Bole', 'Bole Sanitation Service', '+251-11-665-3456', 'sanitation.bole@aaca.gov.et', ST_MakePoint(38.785, 9.00), 'Bole Road'),
('Gullele', 'Gullele Waste Management', '+251-11-665-4567', 'sanitation.gullele@aaca.gov.et', ST_MakePoint(38.73, 9.06), 'Gullele Area'),
('Kirkos', 'Kirkos Sanitation Office', '+251-11-665-5678', 'sanitation.kirkos@aaca.gov.et', ST_MakePoint(38.75, 8.98), 'Kirkos District'),
('Kolfe Keranio', 'Kolfe Sanitation Center', '+251-11-665-6789', 'sanitation.kolfe@aaca.gov.et', ST_MakePoint(38.68, 9.01), 'Kolfe Area'),
('Lideta', 'Lideta Waste Management', '+251-11-665-7890', 'sanitation.lideta@aaca.gov.et', ST_MakePoint(38.71, 8.96), 'Lideta District'),
('Nifas Silk-Lafto', 'Nifas Silk Sanitation Office', '+251-11-665-8901', 'sanitation.nifassilk@aaca.gov.et', ST_MakePoint(38.74, 8.93), 'Nifas Silk Area'),
('Yeka', 'Yeka Sanitation Service', '+251-11-665-9012', 'sanitation.yeka@aaca.gov.et', ST_MakePoint(38.80, 9.03), 'Yeka Sub-City'),
('Akaki Kality', 'Akaki Sanitation Office', '+251-11-665-0123', 'sanitation.akaki@aaca.gov.et', ST_MakePoint(38.80, 8.91), 'Akaki Kality');

-- Sample Sanitation Assets
INSERT INTO sanitation_assets (asset_type, capacity, status, geom) VALUES
('sewer_line', 'medium', 'operational', ST_GeomFromText('LINESTRING(38.75 9.02, 38.76 9.01)', 4326)),
('drainage_canal', 'large', 'operational', ST_GeomFromText('LINESTRING(38.73 9.03, 38.74 9.02)', 4326)),
('waste_collection_point', 'small', 'operational', ST_GeomFromText('LINESTRING(38.785 9.00, 38.79 8.99)', 4326));

-- Sample Tickets (for testing)
INSERT INTO tickets (ticket_number, woreda, issue_description, user_contact, status) VALUES
('SANI-TEST001', 'Bole', 'Overflowing garbage bins', '+251-900-111111', 'SCHEDULED'),
('SANI-TEST002', 'Addis Ketema', 'Sewer blockage causing flooding', '+251-900-222222', 'RESOLVED');
