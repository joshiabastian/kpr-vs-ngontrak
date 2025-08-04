-- db/init_schema.sql

DROP TABLE IF EXISTS rental_prices, house_prices, kpr_scenarios, financial_assumptions, income_profiles, locations CASCADE;

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE rental_prices (
    id SERIAL PRIMARY KEY,
    location_id INT REFERENCES locations(id),
    year INT NOT NULL,
    annual_rent NUMERIC NOT NULL
);

CREATE TABLE house_prices (
    id SERIAL PRIMARY KEY,
    location_id INT REFERENCES locations(id),
    year INT NOT NULL,
    house_type TEXT NOT NULL,
    price NUMERIC NOT NULL
);

CREATE TABLE kpr_scenarios (
    id SERIAL PRIMARY KEY,
    house_price NUMERIC NOT NULL,
    down_payment NUMERIC NOT NULL,
    interest_rate NUMERIC NOT NULL,
    tenor_years INT NOT NULL,
    monthly_installment NUMERIC NOT NULL
);

CREATE TABLE financial_assumptions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    value NUMERIC NOT NULL,
    description TEXT
);

CREATE TABLE income_profiles (
    id SERIAL PRIMARY KEY,
    profile_name TEXT NOT NULL,
    monthly_income NUMERIC NOT NULL,
    year INT NOT NULL,
    notes TEXT
);
