import pandas as pd

def clean_nan(data : pd.DataFrame):
    data.fillna("Unknown")


def clean_datatypes(data : pd.DataFrame):
    for col in data.columns:
        if not 'date' in col.lower():
            continue
        try:
            converted =  pd.to_datetime(data[col] , format='mixed')
            valid_dates = converted.notna().sum()
            # print(valid_dates)

            if valid_dates > len(data) * 0.5:
                data[col] = converted
        except Exception:
            continue