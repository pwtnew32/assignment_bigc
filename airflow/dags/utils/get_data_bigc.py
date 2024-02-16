import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import importlib
import re

def get_data_bigc(list_url):
  list_df = []
  for url in list_url:
    category = str(url).split('/')[-1]
    page = 1
    all_df = []
    while True:
      max_url = f'{url}?page={page}'
      response = requests.get(max_url)
      if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        not_found_element = soup.find('div', class_='category_notfound___mxm0')
        first_div = soup.find('div', {'class':"category_result_row__qfMRp"})
        if not_found_element is None:
          # print(f'-------------------------------- page = {page} --------------------------------------------------')
          for i in first_div:
            product = i.find('div',{'class':'productCard_title__HUSZQ'}).text
            all_price = i.find('div',{'class':'productCard_price__zid5Z'}).text
            price  = str(all_price).split('/')[0].replace(' ','').replace('฿','')
            unit = str(all_price).split('/')[-1].replace(' ','')
            df = pd.DataFrame(columns = [ 'category',
                                          'product',
                                          'brand',
                                          'price_per_unit',
                                          'unit',
                                          'store',
                                          'time_stamp',])
            df['category'] = [category]
            df['product'] = [product]

            # get brand name for each category
            if '-' in category:
                category_search = category.replace('-','_')
            else :
                category_search = category
            list_module = importlib.import_module('utils.list_brand_name_bigc')

            # Use regular expression to find the correct list based on category
            list_regex = re.compile(f'^list_brand_{category_search}', re.IGNORECASE)
            selected_list = [getattr(list_module, var_name) for var_name in dir(list_module) if list_regex.match(var_name)]
            # Check if a list is found
            if selected_list:
                list_brand = selected_list[0]
            else:
                print(f"No list found for category: {category_search}")

            brand_name = ''
            for brand in list_brand:
              if brand.replace(' ','') in product.replace(' ',''):
                brand_name = brand

            if len(brand_name) > 0:
              df['brand'] = [brand_name]
            else:
              df['brand'] = ['อื่นๆ']

            df['price_per_unit'] = [price]
            df['unit'] = [unit]
            # replace blank unit
            df['unit'].replace(to_replace=[''], value='แพ็ค', inplace=True)
            df['store'] = ['BigC']
            df['time_stamp'] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            all_df.append(df)
          page = page + 1
        else:
          break

    final_df = pd.concat(all_df, ignore_index=True)
    list_df.append(final_df)
  # concat all df
  total_df = pd.concat(list_df, ignore_index=False)
  return total_df