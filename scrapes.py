import pandas
import requests
from bs4 import BeautifulSoup

__all__ = ['headers', "Scrapes"]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

class Scrapes:
    # TODO: Consider inheritence...

    @staticmethod
    def scrape_fs_price(fs_url, fs_discount=1):
        if fs_url is not None:
            page = requests.get(fs_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(class_="price-h5")
            price_elems = results.find('span', class_="proPriceFormatted")
            price = float(price_elems.text[1:])
            return round(price * fs_discount, 2)
        else:
            return None

    @staticmethod
    def scrape_fd_price(fd_url, fd_discount=1, fd_threshold=None):
        if fd_url is not None:
            page = requests.get(fd_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            price_elem = soup.find("span", class_="price-sales")
            price = float(price_elem.text[1:])
            if fd_threshold:
                if price > fd_threshold:
                    return round(price * fd_discount, 2)
                return round(price, 2)
            return round(price * fd_discount, 2)
        else:
            return None

    @staticmethod
    def scrape_jl_price(jl_url, jl_discount=1):
        if jl_url is not None:
            page = requests.get(jl_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find(class_="price price--large")
            price = float(result.text[1:])
            return round(price * jl_discount, 2)
        else:
            return None

    @staticmethod
    def scrape_ps_price(ps_url, ps_discount=1, ps_threshold=None, size=None):
        if ps_url is not None:
            try:
                page = requests.get(ps_url, timeout=5, headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                result = soup.findAll(class_="product_variants__wrap")
                for item in result:
                    res_size = item.find('span', class_="product_variants__size")
                    if size == int(res_size.text.split("ML")[0]):
                        res_price = item.find('span', class_="product_variants__price")
                        price = float(res_price.text[1:])
                        if ps_threshold:
                            if price > ps_threshold:
                                return round(price * ps_discount, 2)
                            return round(price, 2)
                        return round(price * ps_discount, 2)
                    else:
                        return None
            except requests.exceptions.ReadTimeout as e:
                print("Read timeout - {}".format(ps_url))
                print(e)
                return None
            except requests.exceptions.ConnectionError as e:
                print("connection error")
                return None
            return None
        else:
            return None
