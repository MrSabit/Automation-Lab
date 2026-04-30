from pathlib import Path
import pandas as pd
import sys
import re
import ast

# add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import RAW_DATA_PATH, PROCESSED_DATA_PATH

# =========================
# LOAD RAW DATA
# =========================
def load_raw_data(filepaths : list):
    print("[LOAD] Loading raw data...")
    dataframes = {}

    for file in filepaths:
        print(f"[LOAD] Loading file {file.name}")
        df = pd.read_csv(file)
        dataframes[file.name]  = df
        print(f"[INFO] Loaded {len(df)} rows")
    return dataframes

# =========================
# CLEAN PRICE
# =========================
def clean_price(price):
    if pd.isna(price):
        return 0.0

    price = str(price)

    if "Free" in price:
        return 0.0

    price = price.replace("$", "").strip()

    try:
        return float(price)
    except:
        return 0.0


# =========================
# CLEAN DISCOUNT
# =========================
def clean_discount(discount):
    if pd.isna(discount):
        return 0

    discount = str(discount)

    discount = discount.replace("%", "").replace("-", "")

    try:
        return int(discount)
    except:
        return 0


# =========================
# CLEAN RATING
# =========================
def clean_rating(rating):
    if pd.isna(rating):
        return None

    rating = str(rating)

    match = re.search(r"([A-Za-z ]+)", rating)

    if match:
        return match.group(1).strip()

    return None


# =========================
# CLEAN GENRES
# =========================
def clean_genres(genres):

    if pd.isna(genres):
        return ""

    # If it's a string like "['FPS', 'Shooter']"
    if isinstance(genres, str):

        try:
            genres = ast.literal_eval(genres)
        except:
            return ""

    # Now genres is a real list
    if isinstance(genres, list):

        # Remove junk values like "+"
        genres = [
            g.strip()
            for g in genres
            if g and g != "+"
        ]

        return ",".join(genres)

    return ""
# =========================
# MAIN CLEANING FUNCTION
# =========================
def clean_dataframe(df : pd.DataFrame):

    print("[CLEAN] Cleaning price...")
    if 'price' in df.columns:
        df["price"] = df["price"].apply(clean_price)
    
    print("[CLEAN] Cleaning discount...")
    if "discount" in df.columns:
        df["discount"] = df["discount"].apply(clean_discount)

    print("[CLEAN] Cleaning rating...")
    if "rating" in df.columns:
        df["rating"] = df["rating"].apply(clean_rating)

    print("[CLEAN] Cleaning genres...")
    if "genres" in df.columns:
        df["genres"] = df["genres"].apply(clean_genres)

    print("[CLEAN] Converting release_date...")
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(
            df["release_date"],
            errors="coerce"
        )

    print("[CLEAN] Removing duplicates...")
    df = df.drop_duplicates(subset="game_id")

    print("[CLEAN] Removing empty titles...")
    if "title" in df.columns:
        df = df.dropna(subset=["title"])

    return df


# =========================
# SAVE CLEAN DATA
# =========================
def save_clean_data(df, filepath):
    print("[SAVE] Saving cleaned data...")
    df.to_csv(filepath, index=False)
    print(f"[DONE] Clean data saved → {filepath}")


# =========================
# PIPELINE RUNNER
# =========================
def run_cleaning_pipeline():

    game_info_path = Path("data/raw/game_info.csv")
    game_detail_path = Path("data/raw/game_detail.csv")

    dfs = load_raw_data([game_info_path, game_detail_path])
    processed_dfs = {}

    for name, df in dfs.items():
        df = clean_dataframe(df)

        print(f"[INFO] Dataframe {name} cleaned")
        processed_dfs[name] = df
        
        save_clean_data(df=df, filepath=PROCESSED_DATA_PATH / name)
        print(f"[INFO] Dataframe {name} Saved")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    run_cleaning_pipeline()