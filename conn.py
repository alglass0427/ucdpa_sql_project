import psycopg2
conn = psycopg2.connect(database="portfolio_db",  
                        user="postgres", 
                        password="Holly#040115",  
                        host="localhost", 
                        port="5432") 

cur = conn.cursor() 

cur.execute( 
'''CREATE TABLE IF NOT EXISTS products (id serial PRIMARY KEY, name varchar(100) NOT NULL UNIQUE, price float  NOT NULL);''') 

# Insert some data into the table 
cur.execute('''INSERT INTO products (name, price) VALUES ('Apple', 1.99), ('Orange', 0.99), ('Banana', 0.59);''')  
conn.commit() 
cur.close() 
# conn.close() 


##https://www.postgresql.org/docs/current/errcodes-appendix.html#ERRCODES-TABLE
sqlstate_errors = {
    '02000': None, # (!) real value is "<class 'psycopg2.errors.NoData'>"
    '02001': None, # (!) real value is "<class 'psycopg2.errors.NoAdditionalDynamicResultSetsReturned'>"
    '03000': None, # (!) real value is "<class 'psycopg2.errors.SqlStatementNotYetComplete'>"
    '08000': None, # (!) real value is "<class 'psycopg2.errors.ConnectionException'>"
    '08001': None, # (!) real value is "<class 'psycopg2.errors.SqlclientUnableToEstablishSqlconnection'>"
    '08003': None, # (!) real value is "<class 'psycopg2.errors.ConnectionDoesNotExist'>"
    '08004': None, # (!) real value is "<class 'psycopg2.errors.SqlserverRejectedEstablishmentOfSqlconnection'>"
    '08006': None, # (!) real value is "<class 'psycopg2.errors.ConnectionFailure'>"
    '08007': None, # (!) real value is "<class 'psycopg2.errors.TransactionResolutionUnknown'>"
    '08P01': None, # (!) real value is "<class 'psycopg2.errors.ProtocolViolation'>"
# -------- Lots of lines ---------- # 
    '23503': None, # (!) real value is "<class 'psycopg2.errors.ForeignKeyViolation'>"
    # There you are!!!
    '23505': None, # (!) real value is "<class 'psycopg2.errors.UniqueViolation'>" 
    # ---------------- 
    '23514': None, # (!) real value is "<class 'psycopg2.errors.CheckViolation'>"
    '23P01': None, # (!) real value is "<class 'psycopg2.errors.ExclusionViolation'>"
}