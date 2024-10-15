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

CREATE_TRANSACTION_MATCHES = '''
            CREATE TABLE IF NOT EXISTS transaction_matches (
                erp_transaction_id INTEGER,
                transaction_id INTEGER,
                matched_amount REAL,
                PRIMARY KEY (erp_transaction_id, transaction_id),
                FOREIGN KEY (erp_transaction_id) references erp_transactions(id),
                FOREIGN KEY (transaction_id) references transactions(id)
            )
'''