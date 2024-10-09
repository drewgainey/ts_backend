# Create GL Accounts table
CREATE_GL_ACCOUNTS_TABLE = '''
             CREATE TABLE IF NOT EXISTS gl_accounts (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 gl_account_number TEXT NOT NULL UNIQUE,
                 gl_account_name TEXT NOT NULL UNIQUE
             )
         '''

INSERT_GL_ACCOUNTS = '''
     INSERT OR IGNORE INTO gl_accounts (gl_account_number, gl_account_name) 
     values ('1000', 'Cash'),
     ('2000', 'Liabilities'),  
     ('3000', 'Equity'),
     ('4000', 'Revenue')  
 '''