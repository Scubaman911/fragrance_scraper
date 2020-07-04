import pandas
from tabulate import tabulate

def discount_to_pc(val):
    res = 1 - (val/100)
    return res

def ingest_csv(csv_path: str):
    data = pandas.read_csv(csv_path)
    df = data.where(data.notnull(), None)
    csv_list = df.values.tolist()
    return csv_list

def display_final_dataframe(scraped_list, scraped_dict):
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
    return tabulate(final_df, headers='keys', tablefmt='psql')