import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import reader

#searchterm = ''

def getsearches(csvfile):
    searches = []
    with open(csvfile, 'r') as f:
        csv_reader = reader(f)
        for row in csv_reader:
            searches.append(row[0])
    return searches

def get_data(searchterm):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        }
        

    url = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&LH_PrefLoc=1&LH_Auction=1&rt=nc&LH_Sold=1&LH_Complete=1'
    print(url)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all("div",class_="s-item__info clearfix")[1:]
    for item in results:
        product = {
            'title': item.find('div', {'class': 's-item__title'}).text,
            'soldprice': float(item.select_one(".s-item__price").find('span', class_='POSITIVE').text.replace('£','').replace(',','').strip()),
            'solddate':  item.select_one(".s-item__title--tagblock").find('span', class_='POSITIVE').text,
            'bids': item.find('span', {'class': 's-item__bids'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    print('Saved to CSV')
    return

for searchterm in getsearches('searches.csv'):
    soup = get_data(searchterm)
    productslist = parse(soup)
    output(productslist, searchterm)
