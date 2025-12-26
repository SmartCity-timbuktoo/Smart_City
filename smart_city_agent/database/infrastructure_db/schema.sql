-- ==========================================
-- Addis-Sync : INFRASTRUCTURE AGENT DATABASE
-- ==========================================

CREATE EXTENSION IF NOT EXISTS postgis;

-- =====================
-- WOREDAS (Geographic Boundaries)
-- =====================
CREATE TABLE woredas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    geom GEOMETRY(POLYGON, 4326) NOT NULL
);

-- =====================
-- INFRASTRUCTURE OFFICES
-- =====================
CREATE TABLE offices (
    id SERIAL PRIMARY KEY,
    woreda VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(100),
    location GEOMETRY(POINT, 4326),
    address TEXT
);

-- =====================
-- INFRASTRUCTURE ASSETS
-- =====================
CREATE TABLE infrastructure_assets (
    id SERIAL PRIMARY KEY,
    asset_type VARCHAR(50), -- road, bridge, sidewalk, streetlight
    condition VARCHAR(30) DEFAULT 'good', -- excellent, good, fair, poor
    geom GEOMETRY(LINESTRING, 4326)
);

-- =====================
-- INFRASTRUCTURE TICKETS
-- =====================
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    woreda VARCHAR(100) NOT NULL,
    issue_description TEXT NOT NULL,
    user_contact VARCHAR(100),
    status VARCHAR(30) DEFAULT 'RECEIVED', -- RECEIVED, INSPECTED, IN_REPAIR, RESOLVED, CLOSED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================
-- INFRASTRUCTURE REPORTS (Historical)
-- =====================
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    report_type VARCHAR(50), -- pothole, crack, bridge_damage, light_failure
    description TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location GEOMETRY(POINT, 4326),
    woreda_id INTEGER REFERENCES woredas(id),
    status VARCHAR(30) DEFAULT 'open'
);

-- =====================
-- INDEXES
-- =====================
CREATE INDEX idx_infrastructure_woredas_geom ON woredas USING GIST (geom);
CREATE INDEX idx_infrastructure_assets_geom ON infrastructure_assets USING GIST (geom);
CREATE INDEX idx_infrastructure_reports_geom ON reports USING GIST (location);
CREATE INDEX idx_infrastructure_tickets_status ON tickets(status);
CREATE INDEX idx_infrastructure_tickets_woreda ON tickets(woreda);
CREATE INDEX idx_infrastructure_offices_woreda ON offices(woreda);
