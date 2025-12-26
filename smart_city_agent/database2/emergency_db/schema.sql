-- ==========================================
-- Addis-Sync : EMERGENCY AGENT DATABASE
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
-- EMERGENCY OFFICES
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
-- EMERGENCY ROUTES
-- =====================
CREATE TABLE emergency_routes (
    id SERIAL PRIMARY KEY,
    route_type VARCHAR(50), -- fire_route, ambulance_path, evacuation_route
    priority_level INTEGER DEFAULT 1,
    geom GEOMETRY(LINESTRING, 4326)
);

-- =====================
-- EMERGENCY TICKETS
-- =====================
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    woreda VARCHAR(100) NOT NULL,
    emergency_type VARCHAR(50), -- fire, medical, accident, evacuation
    issue_description TEXT NOT NULL,
    user_contact VARCHAR(100),
    location_details TEXT,
    status VARCHAR(30) DEFAULT 'RECEIVED', -- RECEIVED, DISPATCHED, RESOLVED, CLOSED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================
-- INCIDENT REPORTS (Historical)
-- =====================
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    incident_type VARCHAR(50),
    severity INTEGER,
    description TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location GEOMETRY(POINT, 4326),
    woreda_id INTEGER REFERENCES woredas(id),
    status VARCHAR(30) DEFAULT 'active'
);

-- =====================
-- INDEXES
-- =====================
CREATE INDEX idx_emergency_woredas_geom ON woredas USING GIST (geom);
CREATE INDEX idx_emergency_routes_geom ON emergency_routes USING GIST (geom);
CREATE INDEX idx_emergency_reports_geom ON reports USING GIST (location);
CREATE INDEX idx_emergency_tickets_status ON tickets(status);
CREATE INDEX idx_emergency_tickets_woreda ON tickets(woreda);
CREATE INDEX idx_emergency_offices_woreda ON offices(woreda);
