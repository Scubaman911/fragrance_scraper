import requests
import pandas
import pprint
from bs4 import BeautifulSoup
from tabulate import tabulate
from collections import OrderedDict
from time import perf_counter
from scrapes import *

fs_discount = 0
fd_discount = 0
jl_discount = 0
ps_discount = 0
ps_threshold = 0
fs_saving = 0.00
fd_saving = 0.00
jl_saving = 0.00
scraped_list = []
scraped_dict = {
    "Name": [],
    "Size": [],
    "fs_price": [],
    "fd_price": [],
    "jl_price": [],
    "ps_price": [],
    "cheapest": [],
    "difference": [],
    "price per mil": [],
}


class Fragrance():
    def __init__(self, name, fs_url, fd_url, jl_url, ps_url, size=0):
        self.properties = {}
        self.properties["name"] = name
        self.properties["fs_url"] = fs_url
        self.properties["fd_url"] = fd_url
        self.properties["jl_url"] = jl_url
        self.properties["ps_url"] = ps_url
        self.properties["size"] = size
        self.properties["prices"] = {}
        self.properties["present_prices"] = {}
        self.calc_prices()
        self.compare()
        self.find_diff()
        self.find_price_per_mil()

    @property
    def name(self):
        # print("name")
        return self.properties.get("name")

    @property
    def size(self):
        # print("size")
        return self.properties.get("size")

    @property
    def fs_price(self):
        # print("fs_price")
        return self.properties["prices"].get("fs_price")

    @property
    def fd_price(self):
        # print("fd_price")
        return self.properties["prices"].get("fd_price")

    @property
    def jl_price(self):
        # print("jl_price")
        return self.properties["prices"].get("jl_price")

    @property
    def ps_price(self):
        # print("ps_price")
        return self.properties["prices"].get("ps_price")

    @property
    def cheapest(self):
        # print("cheapest")
        return self.properties.get("cheapest")

    @property
    def difference(self):
        # print("difference")
        return self.properties.get("difference")

    @property
    def price_per_mil(self):
        # print("ppm")
        return self.properties.get("price_per_mil")

    def calc_prices(self):
        price = Scrapes.scrape_fs_price(
            self.properties.get("fs_url"), fs_discount)
        self.properties["prices"]["fs_price"] = price
        price = Scrapes.scrape_fd_price(
            self.properties.get("fd_url"), fd_discount)
        self.properties["prices"]["fd_price"] = price
        price = Scrapes.scrape_jl_price(
            self.properties.get("jl_url"), jl_discount)
        self.properties["prices"]["jl_price"] = price
        price = Scrapes.scrape_ps_price(
            self.properties.get("ps_url"),
            ps_discount,
            ps_threshold,
            self.size)
        self.properties["prices"]["ps_price"] = price

        # print(self.properties['prices'])

    def compare(self):
        if not self.fs_price and not self.fd_price and not self.jl_price:
            self.properties["cheapest"] = "-"
        else:
            for key, value in self.properties["prices"].items():
                if value:
                    self.properties["present_prices"][key] = value
            if len(self.properties["present_prices"]) > 1:
                min_price = min(
                    self.properties["present_prices"],
                    key=self.properties["prices"].get,
                    default="-"
                )
                self.properties["cheapest"] = min_price
            elif len(self.properties["present_prices"]) == 1:
                for item in self.properties["present_prices"]:
                    self.properties["cheapest"] = item
            else:
                self.properties["cheapest"] = "-"

    def find_diff(self):
        if len(self.properties["present_prices"]) == 0:
            self.compare()
        sorted_prices = sorted(
            self.properties["present_prices"].items(), key=lambda x: x[1])
        if len(sorted_prices) > 1:
            self.properties["difference"] = abs(
                sorted_prices[0][1] - sorted_prices[1][1])
        elif len(sorted_prices) == 1:
            self.properties["difference"] = 0
        else:
            self.properties["difference"] = 0

    def find_price_per_mil(self):
        ppm = self.properties["prices"].get(self.cheapest) / self.size
        self.properties["price_per_mil"] = ppm


def ingest_csv():
    data = pandas.read_csv('fragrances.csv')
    df = data.where(data.notnull(), None)
    for i in range(len(df)):
        name = df['Name'].iloc[i]
        fs_url = df['fs url'].iloc[i]
        fd_url = df['fd url'].iloc[i]
        jl_url = df['jl url'].iloc[i]
        ps_url = df['ps url'].iloc[i]
        size = df['Size'].iloc[i]
        fragrance = Fragrance(name, fs_url, fd_url, jl_url, ps_url, size)
        scraped_list.append(fragrance)


def display_final_dataframe():
    for frag in scraped_list:
        scraped_dict['Name'].append(frag.name)
        scraped_dict['Size'].append(frag.size)
        scraped_dict['fs_price'].append("£{}".format(frag.fs_price))
        scraped_dict['fd_price'].append("£{}".format(frag.fd_price))
        scraped_dict['jl_price'].append("£{}".format(frag.jl_price))
        scraped_dict['ps_price'].append("£{}".format(frag.ps_price))
        scraped_dict['cheapest'].append(frag.cheapest)
        scraped_dict['difference'].append("£{:.2f}".format(frag.difference))
        scraped_dict['price per mil'].append(
            "£{:.2f}".format(frag.price_per_mil))

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
    parser.add_argument("--fs", type=int,
                        help="fragrance shop discount", default=0)
    parser.add_argument("--fd", type=int,
                        help="fragrance direct discount", default=0)
    parser.add_argument("--jl", type=float,
                        help="fragrance direct discount", default=0)
    parser.add_argument("--ps", type=int,
                        help="fragrance direct discount", default=0)
    parser.add_argument("--ps_threshold", type=int,
                        help="fragrance direct discount", default=0)
    args = parser.parse_args()

    fs_discount = discount_to_pc(args.fs)
    fd_discount = discount_to_pc(args.fd)
    jl_discount = discount_to_pc(args.jl)
    ps_discount = discount_to_pc(args.ps)
    ps_threshold = args.ps_threshold
    t1_start = perf_counter()
    main()
    t1_stop = perf_counter()
    print("Time to complete: {}".format(t1_stop-t1))
