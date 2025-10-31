-- Impute example for missing ESG scores
UPDATE esg_data
SET "Total ESG Risk score" = (SELECT AVG("Total ESG Risk score") FROM esg_data WHERE "Total ESG Risk score" IS NOT NULL)
WHERE "Total ESG Risk score" IS NULL;

-- Derive risk_labels (run after loading data)
INSERT INTO risk_labels (symbol, name, risk_flag, compliance_score)
SELECT symbol, name,
       CASE WHEN "ESG Risk Level" IN ('Medium', 'High', 'Severe') THEN 1 ELSE 0 END,
       "Controversy Score"
FROM esg_data;

-- Example clean for financials
UPDATE financial_data
SET "Price/Earnings" = ABS("Price/Earnings") WHERE "Price/Earnings" < 0;