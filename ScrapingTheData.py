import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

is_scraping=True
current_page=1

data=[]

while is_scraping:
    # Make the request
    r = requests.get(f"https://store.fcbarcelona.com/en-eg/collections/best-sellers?page={current_page}").text
    soup = BeautifulSoup(r, 'lxml')
    print(f"Printing page {current_page}")
    
    wrap = soup.find_all('div', class_="card__content card__information")
    # Extract the product name
    product_collection = [wrapy.find('span', class_='card__subtitle').text.strip() 
            for wrapy in wrap if wrapy.find('span', class_='card__subtitle')]
    # Extract the product name
    product_name = [wrapy.find('a', class_="full-unstyled-link").text.strip()
                for wrapy in wrap if wrapy.find('a', class_="full-unstyled-link")]
    # Extract the product price
    price = [wrapy.find('span', class_="price-item price-item--regular").text.strip()
            for wrapy in wrap if wrapy.find('span', class_="price-item price-item--regular")]
    
    data.extend(zip(product_collection, product_name, price)) 
    
    next_page = soup.find_all('a', attrs={'aria-label': re.compile(r'^Page')})
    if next_page:
        current_page += 1
    else:
        is_scraping = False
   
col = ('product_collection', 'product_name', 'price')           
df = pd.DataFrame(data, columns=col)
print(df)

df.to_csv('FCBshop.csv', index=False)

