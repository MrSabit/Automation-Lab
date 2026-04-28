import pandas as pd
import cleaner

data = pd.read_csv('./Projects/Data Cleaner/input_data/messy_data.csv')

def main():
    # print(data)
    # cleaner.clean_nan(data)
    # cleaner.clean_datatypes(data)
    # print(data)
    # print(data.info())
    for col in data.columns:
        if "mail" in col:
           data["MailIndex"] = data[col].str.strip('.')[0]
    print(data)
if __name__ == "__main__":
    main()