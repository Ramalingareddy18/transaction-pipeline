-- PostgreSQL Database Initialization Script
-- Creates the database and applies initial schema

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    date DATE,
    description TEXT,
    amount NUMERIC,
    currency TEXT,
    category TEXT,
    account TEXT,
    transaction_type TEXT,
    month INTEGER,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
CREATE INDEX IF NOT EXISTS idx_transactions_amount ON transactions(amount);
CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account);

-- Create audit log table
CREATE TABLE IF NOT EXISTS transaction_audit (
    audit_id SERIAL PRIMARY KEY,
    transaction_id INTEGER,
    action TEXT,
    old_values JSONB,
    new_values JSONB,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT DEFAULT 'system'
);

-- Grant permissions
GRANT CONNECT ON DATABASE transaction_pipeline_db TO postgres;
GRANT USAGE ON SCHEMA public TO postgres;
GRANT CREATE ON SCHEMA public TO postgres;

-- Log initialization
SELECT NOW() as initialization_time, 'Database initialized successfully' as status;
