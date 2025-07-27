-- Create migrations table if it doesn't exist
CREATE TABLE IF NOT EXISTS applied_migrations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Helper function to execute SQL dynamically
CREATE OR REPLACE FUNCTION execute_sql(query TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE query;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to create migrations table if it doesn't exist
CREATE OR REPLACE FUNCTION create_migrations_table()
RETURNS VOID AS $$
BEGIN
    -- Create the table if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'applied_migrations'
    ) THEN
        CREATE TABLE applied_migrations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        
        RAISE NOTICE 'Created applied_migrations table';
    ELSE
        RAISE NOTICE 'applied_migrations table already exists';
    END IF;
END;
$$ LANGUAGE plpgsql;
