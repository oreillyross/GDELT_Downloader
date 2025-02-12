-- Country table

-- Drop the table if it exists
DROP TABLE IF EXISTS cameo_countries;

-- Create the table
CREATE TABLE cameo_countries (
    code CHAR(3) PRIMARY KEY,
    label VARCHAR(100) NOT NULL
);

-- Copy data from CSV file
-- Note: Update the file path as needed for your environment
\copy cameo_countries FROM 'utils/CAMEO.country.txt' WITH DELIMITER E'\t' CSV HEADER;

-- Add an index on the label for faster lookups (optional)
CREATE INDEX idx_cameo_countries_label ON cameo_countries(label);

-- Verify the import
SELECT COUNT(*) AS total_countries FROM cameo_countries;
--------------------------------------------------------------------------
-- Ethnic groups table

-- Drop the table if it exists
DROP TABLE IF EXISTS cameo_ethnic_groups;

-- Create the table
CREATE TABLE cameo_ethnic_groups (
    code VARCHAR(10) PRIMARY KEY,
    label VARCHAR(100) NOT NULL
);

-- Copy data from CSV file
-- Note: Update the file path as needed for your environment
\copy cameo_ethnic_groups FROM 'utils/CAMEO.ethnic.txt' WITH DELIMITER E'\t' CSV HEADER;

-- Add an index on the label for faster lookups (optional)
CREATE INDEX idx_cameo_ethnic_groups_label ON cameo_ethnic_groups(label);

-- Verify the import
SELECT COUNT(*) AS total_ethnic_groups FROM cameo_ethnic_groups;
--------------------------------------------------------------------------

-- Event codes

-- Drop the table if it exists
DROP TABLE IF EXISTS cameo_event_codes;

-- Create the table
CREATE TABLE cameo_event_codes (
    code VARCHAR(10) PRIMARY KEY,
    event_description TEXT NOT NULL,

    -- Optional: Add hierarchy levels for easier querying
    top_level_code CHAR(2),
    is_top_level BOOLEAN GENERATED ALWAYS AS (length(code) = 2) STORED,
    parent_code VARCHAR(10)
);

-- Copy data from CSV file
-- Note: Update the file path as needed for your environment
\copy cameo_event_codes(code, event_description) FROM 'CAMEO.eventcodes.txt' WITH DELIMITER E'\t' CSV HEADER;

-- Populate additional columns for easier hierarchical analysis
UPDATE cameo_event_codes 
SET 
    top_level_code = SUBSTRING(code FROM 1 FOR 2),
    parent_code = CASE 
        WHEN length(code) > 2 THEN SUBSTRING(code FROM 1 FOR LENGTH(code) - 1)
        ELSE NULL 
    END;

-- Add indexes to support efficient querying
CREATE INDEX idx_cameo_event_codes_top_level ON cameo_event_codes(top_level_code);
CREATE INDEX idx_cameo_event_codes_parent ON cameo_event_codes(parent_code);

-- Verify the import and show some summary statistics
WITH level_counts AS (
    SELECT 
        CASE 
            WHEN length(code) = 2 THEN 'Top Level'
            WHEN length(code) = 3 THEN 'Second Level'
            WHEN length(code) = 4 THEN 'Third Level'
            ELSE 'Other'
        END AS code_level,
        COUNT(*) AS count
    FROM cameo_event_codes
    GROUP BY code_level
)
SELECT 
    (SELECT COUNT(*) FROM cameo_event_codes) AS total_event_codes,
    (SELECT json_object_agg(code_level, count) FROM level_counts) AS level_breakdown;
-------------------------------------------------------------------------------------------
-- Goldstein scale
-- Drop the table if it exists
DROP TABLE IF EXISTS cameo_goldstein_scale;

-- Create the table
CREATE TABLE cameo_goldstein_scale (
    cameo_event_code VARCHAR(10) PRIMARY KEY,
    goldstein_scale DECIMAL(5,2) NOT NULL
);

-- In your PostgreSQL client, you would run this command:
-- \copy cameo_goldstein_scale FROM '/path/to/CAMEO.goldsteinscale.txt' WITH DELIMITER E'\t' CSV HEADER;

-- Alternatively, for a psql script, you might use:
COPY cameo_goldstein_scale FROM '/path/to/CAMEO.goldsteinscale.txt' WITH DELIMITER E'\t' CSV HEADER;
------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS Events;
    
CREATE TABLE Events (
    SQLDATE DATE,
    Title VARCHAR(255),
    EventDescription TEXT,
    Location VARCHAR(255),
    Url VARCHAR(255), CONSTRAINT events_unique_dates_url UNIQUE (SQLDATE, Url)
);
