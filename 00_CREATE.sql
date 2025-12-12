-- Create schema for user (example: "user_arthur")
CREATE SCHEMA IF NOT EXISTS user_arthur AUTHORIZATION root;

SET search_path TO user_arthur;

-- Drop tables if they exist (optional reset)
DROP TABLE IF EXISTS transaction CASCADE;
DROP TABLE IF EXISTS account CASCADE;
DROP TABLE IF EXISTS fiscal_year CASCADE;
DROP TABLE IF EXISTS category CASCADE;

-- Create tables
CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    cashflow_type VARCHAR(20) NOT NULL CHECK (cashflow_type IN ('income', 'expense', 'transfer')),
    description TEXT
);

CREATE TABLE fiscal_year (
    fiscal_year_id SERIAL PRIMARY KEY,
    year INT NOT NULL UNIQUE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE account (
    account_id SERIAL PRIMARY KEY,
    iban VARCHAR(100),
    name VARCHAR(250) NOT NULL,
    nickname VARCHAR(250),
    category_id INT DEFAULT 1,
    type VARCHAR(20) NOT NULL DEFAULT 'external' CHECK (type IN ('internal', 'external')),
    description TEXT,
    CONSTRAINT fk_account_category FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    counterparty_account_id INT,
    date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    balance NUMERIC(12,2) NOT NULL,
    fiscal_id INT NOT NULL,
    description TEXT,
    CONSTRAINT fk_transaction_account FOREIGN KEY (account_id) REFERENCES account(account_id),
    CONSTRAINT fk_transaction_counterparty FOREIGN KEY (counterparty_account_id) REFERENCES account(account_id),
    CONSTRAINT fk_transaction_fiscal FOREIGN KEY (fiscal_id) REFERENCES fiscal_year(fiscal_year_id)
);