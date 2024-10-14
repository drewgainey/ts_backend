CREATE_ERP_TRANSACTIONS_TABLE = '''
              CREATE TABLE IF NOT EXISTS erp_transactions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              erp_transaction_id TEXT NOT NULL,
              amount REAL,
              date DATE,
              description TEXT,
              gl_account_id INTEGER,
              status_id INTEGER,
              accounting_entity_id INTEGER,
              department_id INTEGER
              )
'''