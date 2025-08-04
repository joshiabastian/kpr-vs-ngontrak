-- db/seed/06_financial_assumptions.sql
INSERT INTO financial_assumptions (name, value, description) VALUES
('Inflation Rate', 0.04, 'Asumsi inflasi tahunan 4%'),
('Salary Growth Rate', 0.06, 'Asumsi kenaikan gaji tahunan 6%'),
('Property Appreciation', 0.05, 'Asumsi kenaikan harga rumah 5% per tahun'),
('Rent Increase Rate', 0.03, 'Asumsi kenaikan sewa 3% per tahun');
