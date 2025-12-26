-- ==========================================
-- Addis-Sync : POWER AGENT DATABASE
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
-- POWER DISTRIBUTION OFFICES
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
-- POWER INFRASTRUCTURE
-- =====================
CREATE TABLE power_lines (
    id SERIAL PRIMARY KEY,
    line_type VARCHAR(50), -- transmission_line, distribution_cable, grid_connection
    voltage_kv NUMERIC(6,2),
    status VARCHAR(30) DEFAULT 'active',
    geom GEOMETRY(LINESTRING, 4326)
);

-- =====================
-- POWER TICKETS
-- =====================
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    woreda VARCHAR(100) NOT NULL,
    issue_description TEXT NOT NULL,
    user_contact VARCHAR(100),
    status VARCHAR(30) DEFAULT 'RECEIVED', -- RECEIVED, IN_PROGRESS, RESOLVED, CLOSED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================
-- OUTAGE REPORTS (Historical)
-- =====================
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    report_type VARCHAR(50), -- outage, low_voltage, transformer_failure
    description TEXT,
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location GEOMETRY(POINT, 4326),
    woreda_id INTEGER REFERENCES woredas(id),
    status VARCHAR(30) DEFAULT 'open'
);

-- =====================
-- INDEXES
-- =====================
CREATE INDEX idx_power_woredas_geom ON woredas USING GIST (geom);
CREATE INDEX idx_power_lines_geom ON power_lines USING GIST (geom);
CREATE INDEX idx_power_reports_geom ON reports USING GIST (location);
CREATE INDEX idx_power_tickets_status ON tickets(status);
CREATE INDEX idx_power_tickets_woreda ON tickets(woreda);
CREATE INDEX idx_power_offices_woreda ON offices(woreda);
