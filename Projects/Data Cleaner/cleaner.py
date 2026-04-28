import pandas as pd

def clean_nan(data : pd.DataFrame):
    for col in data.columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            data[col].fillna(data[col].mean(), inplace=True)
        else:
            data[col].fillna("Unknown", inplace=True)


def clean_datatypes(data : pd.DataFrame):
    for col in data.columns:
        # Try to convert to numeric
        try:
            numeric = pd.to_numeric(data[col], errors='coerce')
            if numeric.notna().sum() > len(data) * 0.5:
                data[col] = numeric
                continue
        except:
            pass
        
        # Try to convert to datetime
        try:
            converted = pd.to_datetime(data[col], errors='coerce')
            if converted.notna().sum() > len(data) * 0.5:
                data[col] = converted
                continue
        except:
            pass
        
        # Try to convert to boolean if applicable
        try:
            unique_vals = set(data[col].dropna().unique())
            bool_like = {True, False, 'True', 'False', 'true', 'false', 1, 0, '1', '0'}
            if unique_vals.issubset(bool_like):
                data[col] = data[col].replace({'True': True, 'False': False, 'true': True, 'false': False, '1': True, '0': False})
                data[col] = data[col].astype(bool)
                continue
        except:
            pass
