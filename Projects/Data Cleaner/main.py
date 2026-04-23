import pandas as pd
import cleaner

data = pd.read_csv('./Projects/Data Cleaner/input_data/messy_data.csv')

def main():
    # data.fillna("Unknown" , inplace=True)
    cleaner.clean_datatypes(data)

    print(data.info())
if __name__ == "__main__":
    main()