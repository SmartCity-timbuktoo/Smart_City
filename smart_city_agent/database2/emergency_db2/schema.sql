CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    location GEOMETRY(POINT, 4326) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDING', 'IN_PROGRESS', 'RESOLVED')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    admin_id VARCHAR(50),
    citizen_chat_id VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_location ON reports USING GIST(location);

CREATE OR REPLACE FUNCTION notify_status_change()
RETURNS TRIGGER AS $$
DECLARE
    payload JSON;
BEGIN
    IF NEW.status = 'IN_PROGRESS' AND OLD.status = 'PENDING' THEN
        payload = json_build_object(
            'report_id', NEW.id,
            'user_id', NEW.user_id,
            'status', NEW.status,
            'admin_id', NEW.admin_id,
            'citizen_chat_id', NEW.citizen_chat_id
        );
        PERFORM pg_notify('report_status_change', payload::text);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_status_change ON reports;

CREATE TRIGGER trg_status_change
AFTER UPDATE OF status ON reports
FOR EACH ROW
WHEN (OLD.status = 'PENDING' AND NEW.status = 'IN_PROGRESS')
EXECUTE FUNCTION notify_status_change();
