# Create merchants table
CREATE_MERCHANTS_TABLE = '''
        CREATE TABLE IF NOT EXISTS merchants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_name TEXT NOT NULL UNIQUE,
            logo_url TEXT
        )
    '''
INSERT_INITIAl_MERCHANTS = '''
    INSERT OR IGNORE INTO merchants (merchant_name) values ('No Merchant Available')
'''