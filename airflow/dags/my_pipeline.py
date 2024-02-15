from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
import pendulum
from utils.get_data_bigc import get_data_bigc
from utils.get_data_makro import get_data_makro


# def get_data_bigc(list_url):
#   list_df = []
#   for url in list_url:
#     category = str(url).split('/')[-1]
#     page = 1
#     all_df = []
#     while True:
#       max_url = f'{url}?page={page}'
#       response = requests.get(max_url)
#       if response.status_code == 200:
#         # Parse the HTML content using Beautiful Soup
#         soup = BeautifulSoup(response.content, 'html.parser')
#         not_found_element = soup.find('div', class_='category_notfound___mxm0')
#         first_div = soup.find('div', {'class':"category_result_row__qfMRp"})
#         if not_found_element is None:
#           # print(f'-------------------------------- page = {page} --------------------------------------------------')
#           for i in first_div:
#             product = i.find('div',{'class':'productCard_title__HUSZQ'}).text
#             all_price = i.find('div',{'class':'productCard_price__zid5Z'}).text
#             price  = str(all_price).split('/')[0].replace(' ','').replace('฿','')
#             unit = str(all_price).split('/')[-1].replace(' ','')
#             df = pd.DataFrame(columns = [ 'category',
#                                           'product',
#                                           'brand',
#                                           'price_per_unit',
#                                           'unit',
#                                           'store',
#                                           'time_stamp',])
#             df['category'] = [category]
#             df['product'] = [product]

#             # get brand name for each category
#             if '-' in category:
#                 category_search = category.replace('-','_')
#             else :
#                 category_search = category
#             list_module = importlib.import_module('utils.list_brand_name_bigc')

#             # Use regular expression to find the correct list based on category
#             list_regex = re.compile(f'^list_brand_{category_search}', re.IGNORECASE)
#             selected_list = [getattr(list_module, var_name) for var_name in dir(list_module) if list_regex.match(var_name)]
#             # Check if a list is found
#             if selected_list:
#                 list_brand = selected_list[0]
#             else:
#                 print(f"No list found for category: {category_search}")

#             brand_name = ''
#             for brand in list_brand:
#               if brand.replace(' ','') in product.replace(' ',''):
#                 brand_name = brand

#             if len(brand_name) > 0:
#               df['brand'] = [brand_name]
#             else:
#               df['brand'] = ['อื่นๆ']

#             df['price_per_unit'] = [price]
#             df['unit'] = [unit]
#             df['store'] = ['BigC']
#             df['time_stamp'] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
#             all_df.append(df)
#           page = page + 1
#         else:
#           break

#     final_df = pd.concat(all_df, ignore_index=True)
#     list_df.append(final_df)
#   # concat all df
#   total_df = pd.concat(list_df, ignore_index=False)
#   return total_df

# def get_data_makro(list_url):
#   list_df = []
#   for url in list_url: 
#     category = str(url).split('/')[-1]
#     response = requests.get(url)
#     if response.status_code == 200:
#       # Parse the HTML content using Beautiful Soup
#       soup = BeautifulSoup(response.text, 'html.parser')
#       first_div = soup.find_all('div', {'class':"MuiBox-root css-19sk4h4"})
#       all_df = []
#       for i in first_div:
#         product = i.find('div',{'class':'MuiBox-root css-13q4x2m'}).text
#         brand_name = i.find('div',{'class':'MuiBox-root css-12puazp'}).text
#         try:
#           all_price = i.find('div',{'class':'MuiBox-root css-yeouz0'}).text
#         except:
#           all_price = i.find('div',{'class':'MuiBox-root css-1azjopp'}).text
#         all_price = str(all_price).replace('฿','').replace(',','')
#         unit_text = i.find('div',{'class':'MuiBox-root css-p4myn2'}).text
#         unit_text = unit_text.split(' ')[-1]
#         df = pd.DataFrame(columns = [ 'category',
#                                       'product',
#                                       'brand',
#                                       'price_per_unit',
#                                       'unit',
#                                       'store',
#                                       'time_stamp',])
#         df['category'] = [category]
#         df['product'] = [product]
#         df['brand'] = brand_name
#         df['price_per_unit'] = [all_price]
#         df['unit'] = [unit_text]
#         df['store'] = ['Makro']
#         df['time_stamp'] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
#         all_df.append(df)
#       final_df = pd.concat(all_df,ignore_index=False)
#       list_df.append(final_df)
#       # final_df.to_csv(f'/Users/phawatm/Projects/pyspark_local/web_scraping/makro_{category}.csv', index=False)
#   total_df = pd.concat(list_df, ignore_index=False)
#   total_df['category'] = total_df['category'].replace('drinking-water', 'water')
#   return total_df

@task
def get_data_from_bigc_and_makro(list_url_bigc, list_url_makro):

  bigc_df = get_data_bigc(list_url_bigc)  
  makro_df = get_data_makro(list_url_makro)
  bigc_and_makro_df = pd.concat([bigc_df, makro_df], ignore_index=False)

  return bigc_and_makro_df

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

  bigc_and_makro_df
