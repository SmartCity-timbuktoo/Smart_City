-- Enable PostGIS for location features
CREATE EXTENSION IF NOT EXISTS postgis;

-- ============================================================================
-- 🚑 EMERGENCY AGENT
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS emergency;

CREATE TABLE IF NOT EXISTS emergency.tickets (
    ticket_number TEXT PRIMARY KEY,
    woreda TEXT NOT NULL,
    emergency_type TEXT NOT NULL,
    issue_description TEXT,
    user_contact TEXT,
    location_details TEXT,
    status TEXT DEFAULT 'RECEIVED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS emergency.offices (
    id SERIAL PRIMARY KEY,
    woreda TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    location GEOMETRY(POINT, 4326)
);

-- Mock Data for Emergency
INSERT INTO emergency.offices (woreda, name, phone, email, address, location) VALUES
('Bole', 'Bole Fire Brigade', '+251-11-666-0000', 'fire.bole@addis.gov.et', 'Bole Road, near Airport', ST_SetSRID(ST_MakePoint(38.79, 9.00), 4326)),
('Addis Ketema', 'Addis Ketema Emergency Center', '+251-11-222-1111', 'emer.ak@addis.gov.et', 'Near Piazza', ST_SetSRID(ST_MakePoint(38.74, 9.03), 4326));


-- ============================================================================
-- ⚡ POWER AGENT
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS power;

CREATE TABLE IF NOT EXISTS power.tickets (
    ticket_number TEXT PRIMARY KEY,
    woreda TEXT NOT NULL,
    issue_description TEXT,
    user_contact TEXT,
    status TEXT DEFAULT 'RECEIVED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS power.offices (
    id SERIAL PRIMARY KEY,
    woreda TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    location GEOMETRY(POINT, 4326)
);

-- Mock Data for Power
INSERT INTO power.offices (woreda, name, phone, email, address, location) VALUES
('Bole', 'Bole Power District Office', '+251-11-555-0100', 'power.bole@eep.com.et', 'Bole Michael', ST_SetSRID(ST_MakePoint(38.78, 8.99), 4326));


-- ============================================================================
-- 🗑️ SANITATION AGENT
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS sanitation;

CREATE TABLE IF NOT EXISTS sanitation.tickets (
    ticket_number TEXT PRIMARY KEY,
    woreda TEXT NOT NULL,
    issue_description TEXT,
    user_contact TEXT,
    status TEXT DEFAULT 'RECEIVED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sanitation.offices (
    id SERIAL PRIMARY KEY,
    woreda TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    location GEOMETRY(POINT, 4326)
);

-- Mock Data for Sanitation
INSERT INTO sanitation.offices (woreda, name, phone, email, address, location) VALUES
('Bole', 'Bole Solid Waste Management', '+251-11-618-9999', 'clean.bole@addis.gov.et', 'CMC Road', ST_SetSRID(ST_MakePoint(38.80, 9.01), 4326));


-- ============================================================================
-- 🏗️ INFRASTRUCTURE AGENT
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS infrastructure;

CREATE TABLE IF NOT EXISTS infrastructure.tickets (
    ticket_number TEXT PRIMARY KEY,
    woreda TEXT NOT NULL,
    issue_description TEXT,
    user_contact TEXT,
    status TEXT DEFAULT 'RECEIVED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS infrastructure.offices (
    id SERIAL PRIMARY KEY,
    woreda TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    location GEOMETRY(POINT, 4326)
);

-- Mock Data for Infrastructure
INSERT INTO infrastructure.offices (woreda, name, phone, email, address, location) VALUES
('Bole', 'Bole Roads Authority', '+251-11-646-1234', 'roads.bole@aacra.gov.et', 'Megenagna', ST_SetSRID(ST_MakePoint(38.81, 9.02), 4326));


-- ============================================================================
-- 💧 UTILITY AGENT
-- ============================================================================
CREATE SCHEMA IF NOT EXISTS utility;

CREATE TABLE IF NOT EXISTS utility.tickets (
    ticket_number TEXT PRIMARY KEY,
    woreda TEXT NOT NULL,
    issue_description TEXT,
    user_contact TEXT,
    status TEXT DEFAULT 'RECEIVED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS utility.offices (
    id SERIAL PRIMARY KEY,
    woreda TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    location GEOMETRY(POINT, 4326)
);

-- Mock Data for Utility
INSERT INTO utility.offices (woreda, name, phone, email, address, location) VALUES
('Bole', 'Bole Water & Sewage', '+251-11-662-5555', 'water.bole@aawsa.gov.et', 'Urael', ST_SetSRID(ST_MakePoint(38.77, 9.01), 4326));
