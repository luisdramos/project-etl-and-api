CREATE TABLE etl.charges (
    id TEXT PRIMARY KEY,
    company_id TEXT REFERENCES etl.companies(company_id),
    amount DECIMAL(16,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at DATE,
    updated_at DATE
)