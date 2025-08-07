-- db/init_schema.sql

DROP TABLE IF EXISTS rental_prices;
DROP TABLE IF EXISTS house_prices;
DROP TABLE IF EXISTS kpr_scenarios;
DROP TABLE IF EXISTS financial_assumptions;
DROP TABLE IF EXISTS income_profiles;
DROP TABLE IF EXISTS locations;

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE rental_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    annual_rent REAL NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE house_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    house_type TEXT NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE kpr_scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    house_price REAL NOT NULL,
    down_payment REAL NOT NULL,
    interest_rate REAL NOT NULL,
    tenor_years INTEGER NOT NULL,
    monthly_installment REAL NOT NULL
);

CREATE TABLE financial_assumptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    description TEXT
);

CREATE TABLE income_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_name TEXT NOT NULL,
    monthly_income REAL NOT NULL,
    year INTEGER NOT NULL,
    notes TEXT
);
