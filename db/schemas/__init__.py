from .accounts_schema import CREATE_ACCOUNTS_TABLE, CREATE_INSTITUTIONS_TABLE
from .erp_fields_schema import (CREATE_GL_ACCOUNTS_TABLE, INSERT_GL_ACCOUNTS,
                                CREATE_ACCOUNTING_ENTITIES_TABLE,
                                INSERT_ACCOUNTING_ENTITIES, CREATE_DEPARTMENTS_TABLE,
                                INSERT_DEPARTMENTS)
from .erp_transactions_schema import CREATE_ERP_TRANSACTIONS_TABLE, CREATE_TRANSACTION_MATCHES
from .items_schema import CREATE_ITEMS_TABLE
from .merchants_schema import CREATE_MERCHANTS_TABLE, INSERT_INITIAl_MERCHANTS
from .transactions_schema import CREATE_TRANSACTIONS_TABLE

# Order matters here
ALL_SCHEMAS = [
    #Create any tables that only store plaid information first
    CREATE_ITEMS_TABLE,
    CREATE_INSTITUTIONS_TABLE,
    CREATE_ACCOUNTS_TABLE,
    #Create tables for ERP fields next
    CREATE_GL_ACCOUNTS_TABLE,
    INSERT_GL_ACCOUNTS,
    CREATE_ACCOUNTING_ENTITIES_TABLE,
    INSERT_ACCOUNTING_ENTITIES,
    CREATE_DEPARTMENTS_TABLE,
    INSERT_DEPARTMENTS,
    CREATE_ERP_TRANSACTIONS_TABLE,
    #Create any tables that any transaction tables would depend on
    CREATE_MERCHANTS_TABLE,
    INSERT_INITIAl_MERCHANTS,
    # CREATE_TRANSACTIONS_STATUS_TABLE,
    # INSERT_TRANSACTIONS_STATUS,
    #Create transactions table last
    CREATE_TRANSACTIONS_TABLE,
    CREATE_TRANSACTION_MATCHES,
]