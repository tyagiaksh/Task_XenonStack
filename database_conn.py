import psycopg2
from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: str
  
def connect_to_db():
    try:
        # Connect to your postgres DB
        connection = psycopg2.connect(
            dbname="dataquality",
            user="postgres",
            password="XS.dataops-postgres@321",
            host="172.16.200.229",
            port="30387"
        )
        # connection = psycopg2.connect(
        #     dbname=db_config.dbname,
        #     user=db_config.user,
        #     password=db_config.password,
        #     host=db_config.host,
        #     port=db_config.port
        # )
        return connection
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None

def get_table_names(conn):
    try:
        cur=conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        result=cur.fetchall()
        table=[]
        for res in result:
            table.append(res[0])
        return table
    except Exception as error:
        print(f"Error executing query: {error}")
        return None
   
def get_sample_data(conn, schema_name, table_name, limit=2):
    try:
        cur = conn.cursor()
        
        # Fetch column names
        column_query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s;
        """
        cur.execute(column_query, (schema_name, table_name))
        columns = [col[0] for col in cur.fetchall()]
        # Fetch rows
        row_query = f"SELECT * FROM {schema_name}.{table_name} LIMIT %s;"
        cur.execute(row_query, (limit,))
        rows = cur.fetchall()
        
        cur.close()
        # Combine column names and rows
        result = [dict(zip(columns, row)) for row in rows]
        return result
    except Exception as error:
        print(f"Error fetching rows for table {schema_name}.{table_name}: {error}")
        return [] 
