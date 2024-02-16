import yaml
import numpy as np
from sqlalchemy import create_engine



def load_df_to_db(df, table_name):

  with open('/opt/airflow/config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

  pslq_connection = config['connections']['postgresql_connection']
  host = pslq_connection['host']
  port = pslq_connection['port']
  database_name = pslq_connection['database_name']
  schema_name = pslq_connection['schema']
  username = pslq_connection['username']
  password = pslq_connection['password']
  connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'

  # Create a SQLAlchemy engine
  engine = create_engine(connection_string)

  # check df have records
  if len(df) > 0:
    try:
        conn = engine.connect()
        
        # Load the DataFrame into PostgreSQL using df.to_sql
        df.to_sql(name=table_name, schema=schema_name, con=conn, if_exists='replace', index=False)
        # Close the connection
        # conn.commit()
        conn.close()
        print('load success!!')
    except Exception as e:
      raise e
  else:
    print('no data')