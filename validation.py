
class Validation:
    @staticmethod
    def none_price_check(site, name, price):
        if not price:
            print("Price from {} for {} not available.".format(site, name))
