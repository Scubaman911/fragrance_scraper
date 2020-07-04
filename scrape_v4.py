import pandas
from data_handling import FragranceDataObject, scraped_dict
from utils import display_final_dataframe


if __name__ == "__main__":
    frag_obj = FragranceDataObject.create_frags_from_csv("fragrances.csv")
    frag_obj.process_fragrances()
    tab = display_final_dataframe(frag_obj.fragrance_list, scraped_dict)
    print(tab)
