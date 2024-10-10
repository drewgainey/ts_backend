# Create Accounting Entities Table
CREATE_ACCOUNTING_ENTITIES_TABLE = """
        CREATE TABLE IF NOT EXISTS accounting_entities (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 entity_identifier TEXT NOT NULL UNIQUE,
                 entity_name TEXT NOT NULL UNIQUE
        )
"""
INSERT_ACCOUNTING_ENTITIES = """
     INSERT OR IGNORE INTO accounting_entities (entity_identifier, entity_name) 
     values ('100', 'ABC Corp'),
     ('200', 'XYZ LLC')
"""

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

# Create Departments
CREATE_DEPARTMENTS_TABLE =  '''
        CREATE TABLE IF NOT EXISTS departments (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 department TEXT NOT NULL UNIQUE
        )
'''
INSERT_DEPARTMENTS = '''
    INSERT OR IGNORE INTO departments (department) 
     values ('Sales'),
     ('Operations'),
     ('Engineering')
'''