from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as req
from datetime import datetime
import pandas as pd

LAST_PAGE_NUMBER = 2
BASE_URL = "https://www.lamoda.ru/c/4152/default-men/?page="



timestamp = datetime.now().strftime("%Y-%m-%d")
brand = []
prices = []
type = []
lns = []


for a in range(1, LAST_PAGE_NUMBER):
    my_url = BASE_URL + str(a)
    page = req(my_url)
    page_html = page.read()
    page.close()
    print(f'page {a} scanning...')
    # html prasing
    page_soup = bsoup(page_html, "html.parser")

# grab the info
    products = page_soup.findAll('div', class_="x-product-card__card")

    for data in products:
        links = data.findAll('a', href=True)
        #print(links)
        for link in links:
            y = link['href']
            #print(link)

            lns.append(y)
            #print(lns)
            dt = link.findAll('div', class_="x-product-card-description")
            # print(dt)

            for data in dt:

                br = data.findAll('div', class_="x-product-card-description__brand-name")
                brtype = data.findAll('div', class_='x-product-card-description__product-name')
                for datab in br:
                    brand_name = datab.text
                    brand.append(brand_name)
                    #print(brand)
                for datat in brtype:
                    type_name = datat.text
                    type.append(type_name)
                    #print(type)

                search = []
                search_f = []

                discounts = data.findAll('span',
                                        class_="x-product-card-description__price-new x-product-card-description__price-WEB8507_price_no_bold")

                orginals = data.findAll('span',
                                        class_="x-product-card-description__price-single x-product-card-description__price-WEB8507_price_no_bold")
                search.append(discounts)
                search_f.append(orginals)
                #print(orginals)
                #print(search)
                for i in range(len(search)):
                    #print(search[i])
                    if search[i] != "[]":
                        for data_ds in discounts:
                            discount = data_ds.text
                            #print(discount)
                            prices.append(discount)

                    if search_f != "[]":
                        for data_or in orginals:
                            orginal = data_or.text
                            prices.append(orginal)
                            #print(orginal)

#print(prices)
fieldnames = ['Brand', 'Type', 'Price', 'Currency', 'Link']

last = []

for i in range(len(prices)):

    a = {
            'Brand': brand[i],
            'Type': type[i],
            'Price': prices[i],
            'Currency': 'RUB',
            'Link': f'https://www.lamoda.ru/{lns[i]}/'
        }
    last.append(a)

df = pd.DataFrame(last, columns=fieldnames)

print(df)
df.to_csv(f'outputfile{timestamp}.csv')
