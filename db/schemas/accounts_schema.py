# Create accounts table if it doesn't exist
CREATE_ACCOUNTS_TABLE = '''
          CREATE TABLE IF NOT EXISTS accounts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              account_id TEXT NOT NULL,
              item_id TEXT NOT NULL,
              account_name TEXT NOT NULL,
              account_official_name TEXT NOT NULL,
              account_type TEXT NOT NULL,
              account_subtype TEXT NOT NULL,
              mask INTEGER,
              balance_available REAL,
              balance_current REAL,
              balance_limit REAL,
              currency TEXT NOT NULL)
      '''
