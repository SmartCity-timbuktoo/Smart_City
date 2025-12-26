-- ==========================================
-- Addis-Sync : UTILITY AGENT DATABASE
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
-- UTILITY OFFICES
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
-- UTILITY INFRASTRUCTURE
-- =====================
CREATE TABLE utilities (
    id SERIAL PRIMARY KEY,
    utility_type VARCHAR(50), -- water_pipe, sewer_pipe, hydraulic_line
    pressure_level NUMERIC(5,2),
    status VARCHAR(30) DEFAULT 'operational',
    geom GEOMETRY(LINESTRING, 4326)
);

-- =====================
-- UTILITY TICKETS
-- =====================
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    woreda VARCHAR(100) NOT NULL,
    issue_description TEXT NOT NULL,
    user_contact VARCHAR(100),
    status VARCHAR(30) DEFAULT 'RECEIVED', -- RECEIVED, ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================
-- UTILITY REPORTS (Historical)
-- =====================
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    issue_type VARCHAR(50), -- leak, low_pressure, contamination
    description TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location GEOMETRY(POINT, 4326),
    woreda_id INTEGER REFERENCES woredas(id),
    status VARCHAR(30) DEFAULT 'open'
);

-- =====================
-- INDEXES
-- =====================
CREATE INDEX idx_utility_woredas_geom ON woredas USING GIST (geom);
CREATE INDEX idx_utility_utilities_geom ON utilities USING GIST (geom);
CREATE INDEX idx_utility_reports_geom ON reports USING GIST (location);
CREATE INDEX idx_utility_tickets_status ON tickets(status);
CREATE INDEX idx_utility_tickets_woreda ON tickets(woreda);
CREATE INDEX idx_utility_offices_woreda ON offices(woreda);
