CREATE OR REPLACE VIEW etl.daily_company_totals AS
SELECT 
    c.company_id,
    c.name,
    ch.created_at AS transaction_date,
    SUM(ch.amount) AS total_amount
FROM etl.charges ch
JOIN etl.companies c ON ch.company_id = c.company_id
GROUP BY c.company_id, c.name, ch.created_at
ORDER BY transaction_date;
