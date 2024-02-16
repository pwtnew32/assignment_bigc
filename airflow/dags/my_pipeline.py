from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
import pendulum
from utils.get_data_bigc import get_data_bigc
from utils.get_data_makro import get_data_makro
from utils.load_df_to_db import load_df_to_db

@task
def get_data_from_bigc_and_makro(list_url_bigc, list_url_makro):

  bigc_df = get_data_bigc(list_url_bigc)  
  makro_df = get_data_makro(list_url_makro)
  bigc_and_makro_df = pd.concat([bigc_df, makro_df], ignore_index=False)

  return bigc_and_makro_df

@task
def load_to_db(df, table_name):
  load_df_to_db(df, table_name)

default_args = {
  'owner': 'Admin',
  'start_date': datetime.today() - timedelta(days = 1)
  }

with DAG(dag_id='my_pipeline',
  schedule_interval=None,
  default_args=default_args,
  schedule='0 1 * * *',
  start_date=pendulum.datetime(2024, 1, 10, tz="Asia/Bangkok"),
  catchup=False
  ) as dag:

  list_url_bigc = ['https://www.bigc.co.th/category/vegetables', 
    'https://www.bigc.co.th/category/meat', 
    'https://www.bigc.co.th/category/water',
    'https://www.bigc.co.th/category/washing-machine'
    ]
  list_url_makro = ['https://www.makro.pro/c/fruit-vegetables/vegetables' ,
  'https://www.makro.pro/c/meat', 
  'https://www.makro.pro/c/beverages/drinking-water', 
  'https://www.makro.pro/c/electronics/washing-machine']


  bigc_and_makro_df = get_data_from_bigc_and_makro(list_url_bigc, list_url_makro)
  table_name = 'products'
  load_to_db = load_to_db(bigc_and_makro_df, table_name)
  
  bigc_and_makro_df >> load_to_db
