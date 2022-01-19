from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as req
from datetime import datetime
import pandas as pd

timestamp = datetime.now().strftime("%Y-%m-%d")
brand = []
pri = []
type = []
lns = []
discount = []
for a in range(1, 16):
    my_url = "https://www.lamoda.ru/c/4152/default-men/?page=" + str(a)
    page = req(my_url)
    page_html = page.read()
    page.close()
    print(f'page {a} scanning...')
    # html prasing
    page_soup = bsoup(page_html, "html.parser")

    # grab the info
    products = page_soup.findAll('div', class_="products-catalog__list")

    for data in products:
        links = data.findAll('a', href=True)

    for link in links:
        y = link['href']
        # print(link)
        lns.append(y)
        # print(link)
        dt = link.findAll('div', class_="to-favorites js-to-favorites to-favorites_wish-groups")
        # print(dt)

        for data in dt:
            x = data['data-brand']
            brand.append(x)
            x = data['data-name']
            type.append(x)
            if data.has_key("data-discount") == True:
                x = data['data-price']
                pri.append(x)
                y = data['data-discount-percent']
                discount.append(y)
            if data.has_key("data-discount") == False:
                x = data['data-price-origin']
                pri.append(x)
                discount.append(0)

fieldnames = ['Brand', 'Type', 'Price', 'Currency', 'Discount', 'Link']

last = []

for i in range(len(pri)):
    a = {'Brand': brand[i], 'Type': type[i], 'Price': pri[i], 'Currency': 'RUB',
         'Link': f'https://www.lamoda.ru/{lns[i]}/', 'Discount': discount[i]}
    last.append(a)

df = pd.DataFrame(last, columns=fieldnames)
# df = df.drop('type', axis=1)
print(df)
df.to_csv(f'outputfile{timestamp}.csv')
