# Web scraper for fragrance shop and fragrance direct for most commonly recommended fragrances
#
# To Do:
# - Add a price per mil feature
#
import requests
import pandas
import pprint
from bs4 import BeautifulSoup
from tabulate import tabulate
from collections import OrderedDict

fs_discount = 0
fd_discount = 0
fs_saving = 0.00
fd_saving = 0.00
jl_saving = 0.00
final_df = None
scraped_list = []
scraped_dict = {
    "Name": [],
    "Size": [],
    "fs_price": [],
    "fd_price": [],
    "jl_price": [],
    "cheapest": [],
    "difference": [],
    "price per mil": [],
}


class Scraped_Fragrance():
    def __init__(self, name, fs_url, fd_url, jl_url, size):
        self.name = name
        self.size = size
        self.fs_url = fs_url
        self.fd_url = fd_url
        self.jl_url = jl_url
        self.prices = {
            "FS": self.scrape_fs_price(),
            "FD": self.scrape_fd_price(),
            "JL": self.scrape_jl_price(),
        }
        self.present_prices = {}
        self.cheapest = self.compare()
        self.difference = self.find_diff()
        self.price_per_mil = self.price_per_mil()

    def scrape_fs_price(self):
        if self.fs_url is not None:
            page = requests.get(self.fs_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(class_="price-h5")
            price_elems = results.find('span', class_=None)
            price = float(price_elems.text[1:])
            return round(price * fs_discount, 2)
        else:
            print("{} - fs url not available".format(self.name))
            return None

    def scrape_fd_price(self):
        if self.fd_url is not None:
            page = requests.get(self.fd_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            price_elem = soup.find("span", class_="price-sales")
            price = float(price_elem.text[1:])
            return round(price * fd_discount, 2)
        else:
            print("{} - fd url not available".format(self.name))
            return None

    def scrape_jl_price(self):
        if self.jl_url is not None:
            page = requests.get(self.jl_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            result = soup.find(class_="price price--large")
            price = float(result.text[1:])
            return round(price, 2)
        else:
            print("{} - jl url not available".format(self.name))
            return None

    def compare(self):
        global fs_saving
        global fd_saving
        global jl_saving
        if not self.prices["FS"] and not self.prices["FD"] and not self.prices["JL"]:
            return "-"
        else:
            for key, value in self.prices.items():
                if value:
                    self.present_prices[key] = value
            if len(self.present_prices) > 1:
                min_price = min(self.present_prices, key=self.prices.get, default="-")
                return min_price
            elif len(self.present_prices) == 1:
                for item in self.present_prices:
                    return item
            else:
                return "-"

    def find_diff(self):
        sorted_prices = sorted(self.present_prices.items(), key = lambda x : x[1])
        if len(sorted_prices) > 1:
            return abs(sorted_prices[0][1] - sorted_prices[1][1])
        elif len(sorted_prices) == 1:
            return 0
        else:
            return 0

    def price_per_mil(self):
        ppm = self.prices[self.cheapest] / self.size
        return ppm


def ingest_csv():
    data = pandas.read_csv('fragrances.csv')
    df = data.where(data.notnull(), None)
    for i in range(len(df)):
        name = df['Name'].iloc[i]
        fs_url = df['fs url'].iloc[i]
        fd_url = df['fd url'].iloc[i]
        jl_url = df['jl url'].iloc[i]
        size = df['Size'].iloc[i]
        fragrance = Scraped_Fragrance(name, fs_url, fd_url, jl_url, size)
        scraped_list.append(fragrance)


def display_final_dataframe():
    for frag in scraped_list:
        scraped_dict['Name'].append(frag.name)
        scraped_dict['Size'].append(frag.size)
        scraped_dict['fs_price'].append("£{}".format(frag.prices["FS"]))
        scraped_dict['fd_price'].append("£{}".format(frag.prices["FD"]))
        scraped_dict['jl_price'].append("£{}".format(frag.prices["JL"]))
        scraped_dict['cheapest'].append(frag.cheapest)
        scraped_dict['difference'].append("£{:.2f}".format(frag.difference))
        scraped_dict['price per mil'].append("£{:.2f}".format(frag.price_per_mil))

    final_df = pandas.DataFrame(scraped_dict)
    print(tabulate(final_df, headers='keys', tablefmt='psql'))


def discount_to_pc(val):
    res = 1 - (val/100)
    return res


def main():
    ingest_csv()
    display_final_dataframe()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fs_discount", type=int,
                        help="fragrance shop discount", default=0)
    parser.add_argument("--fd_discount", type=int,
                        help="fragrance direct discount", default=0)
    args = parser.parse_args()

    fs_discount = discount_to_pc(args.fs_discount)
    fd_discount = discount_to_pc(args.fd_discount)

    main()
