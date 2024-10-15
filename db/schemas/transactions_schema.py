# Create transactions table
CREATE_TRANSACTIONS_TABLE = '''
          CREATE TABLE IF NOT EXISTS transactions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              transaction_id TEXT NOT NULL,
              account_id TEXT NOT NULL,
              amount REAL,
              date DATE,
              description TEXT,
              merchant_id INTEGER,
              currency TEXT NOT NULL,
              pending BOOLEAN,
             -- gl_account_id INTEGER,
             -- status_id INTEGER,
             -- accounting_entity_id INTEGER,
             -- department_id INTEGER,
              FOREIGN KEY(account_id) REFERENCES accounts(account_id),
              FOREIGN KEY(merchant_id) REFERENCES merchants(id)
            -- FOREIGN KEY(gl_account_id) REFERENCES gl_accounts(id),
            -- FOREIGN KEY(status_id) REFERENCES transactions_status(id),
            -- FOREIGN KEY(accounting_entity_id) REFERENCES accounting_entities(id),
            -- FOREIGN KEY (department_id) REFERENCES departments(id) 
              )
      '''
# Create transactions status table
# CREATE_TRANSACTIONS_STATUS_TABLE='''
#            CREATE TABLE IF NOT EXISTS transactions_status (
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                status TEXT NOT NULL UNIQUE)
#        '''
# INSERT_TRANSACTIONS_STATUS='''
#        INSERT OR IGNORE INTO
#           transactions_status (status)
#       values
#       ('unclassified'),
#       ('unmatched'),
#       ('matched')
#    '''
