CREATE DATABASE IF NOT EXISTS finances_db;
USE finances_db;

DROP TABLE IF EXISTS transaction, account, fiscal_year, category;

CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    cashflow_type ENUM('income','expense','transfer') NOT NULL,
    description TEXT
);

CREATE TABLE fiscal_year (
    fiscal_year_id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL UNIQUE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE account (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    iban VARCHAR(100),
    name VARCHAR(250) NOT NULL,
    nickname VARCHAR(250),
    category_id INT DEFAULT 1,
    type ENUM('internal','external') NOT NULL DEFAULT 'external',
    description TEXT
);

CREATE TABLE transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    counterparty_account_id INT,
    date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    balance DECIMAL(12,2) NOT NULL,
    fiscal_id INT NOT NULL,
    description TEXT
);

-- Add foreign keys separately
ALTER TABLE account
ADD CONSTRAINT fk_account_category
FOREIGN KEY (category_id) REFERENCES category(category_id);

ALTER TABLE transaction
ADD CONSTRAINT fk_transaction_account
FOREIGN KEY (account_id) REFERENCES account(account_id);

ALTER TABLE transaction
ADD CONSTRAINT fk_transaction_counterparty
FOREIGN KEY (counterparty_account_id) REFERENCES account(account_id);

ALTER TABLE transaction
ADD CONSTRAINT fk_transaction_fiscal
FOREIGN KEY (fiscal_id) REFERENCES fiscal_year(fiscal_year_id);
