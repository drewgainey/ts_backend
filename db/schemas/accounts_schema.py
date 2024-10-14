CREATE_INSTITUTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS institutions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              plaid_institution_id TEXT NOT NULL,
              institution_name TEXT NOT NULL
        )
'''




CREATE_ACCOUNTS_TABLE = '''
          CREATE TABLE IF NOT EXISTS accounts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              account_id TEXT NOT NULL,
              institution_id INTEGER,
              item_id TEXT NOT NULL,
              account_name TEXT NOT NULL,
              account_official_name TEXT NOT NULL,
              account_type TEXT NOT NULL,
              account_subtype TEXT NOT NULL,
              mask INTEGER,
              balance_available REAL,
              balance_current REAL,
              balance_limit REAL,
              currency TEXT NOT NULL,
              FOREIGN KEY(institution_id) REFERENCES institutions(id)
              )
      '''
