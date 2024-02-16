import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import importlib

def get_data_makro(list_url):
  list_df = []
  for url in list_url: 
    category = str(url).split('/')[-1]
    response = requests.get(url)
    if response.status_code == 200:
      # Parse the HTML content using Beautiful Soup
      soup = BeautifulSoup(response.text, 'html.parser')
      first_div = soup.find_all('div', {'class':"MuiBox-root css-19sk4h4"})
      all_df = []
      for i in first_div:
        product = i.find('div',{'class':'MuiBox-root css-13q4x2m'}).text
        brand_name = i.find('div',{'class':'MuiBox-root css-12puazp'}).text
        try:
          all_price = i.find('div',{'class':'MuiBox-root css-yeouz0'}).text
        except:
          all_price = i.find('div',{'class':'MuiBox-root css-1azjopp'}).text
        all_price = str(all_price).replace('฿','').replace(',','')
        unit_text = i.find('div',{'class':'MuiBox-root css-p4myn2'}).text
        unit_text = unit_text.split(' ')[-1]
        df = pd.DataFrame(columns = [ 'category',
                                      'product',
                                      'brand',
                                      'price_per_unit',
                                      'unit',
                                      'store',
                                      'time_stamp',])
        df['category'] = [category]
        df['product'] = [product]
        df['brand'] = brand_name
        df['price_per_unit'] = [all_price]
        df['unit'] = [unit_text]
        df['store'] = ['Makro']
        df['time_stamp'] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        all_df.append(df)
      final_df = pd.concat(all_df,ignore_index=False)
      list_df.append(final_df)
      # final_df.to_csv(f'/Users/phawatm/Projects/pyspark_local/web_scraping/makro_{category}.csv', index=False)
  total_df = pd.concat(list_df, ignore_index=False)
  total_df['category'] = total_df['category'].replace('drinking-water', 'water')
  return total_df