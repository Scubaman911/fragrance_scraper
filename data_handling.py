import pandas
from scrapes import *


def ingest_csv(csv_path: str):
    data = pandas.read_csv(csv_path)
    df = data.where(data.notnull(), None)
    csv_list = df.values.tolist()
    return csv_list


class FragranceDataObject():

    def __init__(self, fragrances):
        self.fragrance_list = fragrances

    @staticmethod
    def csv_entry_to_frag(entry):
        name = entry[0]
        size = entry[1]
        fs_url = entry[2]
        fd_url = entry[3]
        jl_url = entry[4]
        ps_url = entry[5]
        fragrance = Fragrance(name, size, fs_url, fd_url, jl_url, ps_url)
        return fragrance
        # scraped_list.append(fragrance)

    @classmethod
    def create_frags_from_csv(cls, csv_path):
        csv_list = ingest_csv(csv_path)
        frags = []
        for entry in csv_list:
            frag = cls.csv_entry_to_frag(entry)
            frags.append(frag)
        return cls(frags)

    def process_fragrances(self):
        frags = self.fragrance_list
        for frag in frags:
            frag.process_all_attributes()


class Fragrance():
    def __init__(self, name, size, fs_url, fd_url, jl_url, ps_url):
        self.properties = {}
        self.properties["name"] = name
        self.properties["fs_url"] = fs_url
        self.properties["fd_url"] = fd_url
        self.properties["jl_url"] = jl_url
        self.properties["ps_url"] = ps_url
        self.properties["size"] = size
        self.properties["prices"] = {}
        self.properties["present_prices"] = {}

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

    def process_all_attributes(self):
        self._calc_prices()
        self._compare()
        self._find_diff()
        self._find_price_per_mil()

    def _calc_prices(self):
        price = Scrapes.scrape_fs_price(
            self.properties.get("fs_url"), fs_discount)
        self.properties["prices"]["fs_price"] = price
        print("{} fs calculated: {}".format(self.name, price))
        price = Scrapes.scrape_fd_price(
            self.properties.get("fd_url"), fd_discount, fd_threshold)
        self.properties["prices"]["fd_price"] = price
        print("{} fd calculated: {}".format(self.name, price))
        price = Scrapes.scrape_jl_price(
            self.properties.get("jl_url"), jl_discount)
        self.properties["prices"]["jl_price"] = price
        print("{} jl calculated: {}".format(self.name, price))
        # price = None
        price = Scrapes.scrape_ps_price(
            self.properties.get("ps_url"),
            ps_discount,
            ps_threshold,
            self.size)
        print("{} ps calculated: {}".format(self.name, price))
        self.properties["prices"]["ps_price"] = price
        # print(self.properties["prices"])

    def _compare(self):
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

    def _find_diff(self):
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

    def _find_price_per_mil(self):
        ppm = self.properties["prices"].get(self.cheapest) / self.size
        self.properties["price_per_mil"] = ppm


if __name__ == "__main__":
    frag_obj = FragranceDataObject.create_frags_from_csv("fragrances.csv")
    print(frag_obj.fragrance_list[0].name)
    print(frag_obj.fragrance_list[0].size)
    print(len(frag_obj.fragrance_list))