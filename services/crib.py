import requests
from bs4 import BeautifulSoup

def scrape(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    imgs = soup.select(".owl-lazy")
    address = soup.find(attrs={ 'itemprop': 'streetAddress' })
    city = soup.find(attrs={ 'itemprop': 'addressLocality' })
    state = soup.find(attrs={ 'itemprop': 'addressRegion' })
    price = soup.find(attrs={ 'itemprop': 'price' })

    full_name = address.text + ' ' + city.text + ', ' + state.text

    pictures = []

    for e in imgs:
        split_url = e.attrs['data-src'].split('_')
        if split_url[1] == 'h770' and e.attrs['data-src'] not in pictures:
            pictures.append(e.attrs['data-src'])

    return {
        'name': full_name,
        'pictures': '|'.join(pictures),
        'price': price.attrs['content']
    }
