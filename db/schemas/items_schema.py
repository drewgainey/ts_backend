# Create access tokens table
CREATE_ITEMS_TABLE = '''
       CREATE TABLE IF NOT EXISTS items (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           item_id TEXT NOT NULL,
           access_token TEXT UNIQUE NOT NULL,
           transactions_cursor TEXT UNIQUE
       )
   '''