CREATE TABLE IF NOT EXISTS hsts
(
    url        TEXT PRIMARY KEY,
    status     TEXT,
    updated_at TIMESTAMP DEFAULT now()
);
