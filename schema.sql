CREATE TABLE IF NOT EXISTS hsts
(
    url        TEXT PRIMARY KEY,
    status     TEXT,
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS web_risk
(
    url                TEXT PRIMARY KEY,
    social_engineering BOOLEAN DEFAULT FALSE,
    malware            BOOLEAN DEFAULT FALSE,
    expire_time        TIMESTAMP
);

CREATE TABLE IF NOT EXISTS past_checks
(
    url        TEXT PRIMARY KEY,
    data       JSONB,
    created_at TIMESTAMP DEFAULT now()
);