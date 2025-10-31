-- sql/schema.sql
DROP TABLE IF EXISTS esg_data;
DROP TABLE IF EXISTS financial_data;
DROP TABLE IF EXISTS risk_labels;
DROP VIEW IF EXISTS merged_data_view;

CREATE TABLE esg_data (
    company_id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    sector TEXT,
    total_esg_risk_score REAL,
    environment_risk_score REAL,
    social_risk_score REAL,
    governance_risk_score REAL,
    controversy_level TEXT,
    controversy_score REAL,
    esg_risk_percentile TEXT,
    esg_risk_level TEXT,
    risk_flag INTEGER  -- ADD THIS
);

CREATE TABLE financial_data (
    company_id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    sector TEXT,
    price REAL,
    price_earnings REAL,
    dividend_yield REAL,
    earnings_share REAL,
    market_cap INTEGER,
    ebitda INTEGER,
    price_sales REAL,
    price_book REAL,
    debt_to_equity REAL,
    roe REAL
);

CREATE TABLE risk_labels (
    company_id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    risk_flag INTEGER CHECK (risk_flag IN (0,1)),
    compliance_score REAL
);

CREATE VIEW merged_data_view AS
SELECT 
    e.symbol, 
    e.name AS name, 
    e.sector, 
    e.total_esg_risk_score AS esg_score,
    e.environment_risk_score,
    e.social_risk_score,
    e.governance_risk_score,
    f.price_book AS debt_to_equity_proxy,
    f.roe AS roe_proxy,
    r.risk_flag
FROM esg_data e
JOIN financial_data f ON e.symbol = f.symbol
JOIN risk_labels r ON e.symbol = r.symbol;