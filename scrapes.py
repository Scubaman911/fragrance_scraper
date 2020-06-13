import pandas
import requests
from bs4 import BeautifulSoup


class Scrapes:
    # TODO: Consider inheritence...

    @staticmethod
    def scrape_fs_price(fs_url, fs_discount=1):
        if fs_url is not None:
            page = requests.get(fs_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(class_="price-h5")
            price_elems = results.find('span', class_=None)
            price = float(price_elems.text[1:])
            return round(price * fs_discount, 2)
        else:
            return None

    @staticmethod
    def scrape_fd_price(fd_url, fd_discount=1):
        if fd_url is not None:
            page = requests.get(fd_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            price_elem = soup.find("span", class_="price-sales")
            price = float(price_elem.text[1:])
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
    def scrape_ps_price(ps_url, ps_discount, ps_threshold, size):
        if ps_url is not None:
            page = requests.get(ps_url)
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
            return None
        else:
            return None
