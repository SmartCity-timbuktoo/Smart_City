CREATE TABLE utility_tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(30) UNIQUE NOT NULL,
    woreda VARCHAR(100) NOT NULL,
    issue_description TEXT NOT NULL,
    user_contact VARCHAR(100),
    status VARCHAR(30) NOT NULL DEFAULT 'RECEIVED',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
