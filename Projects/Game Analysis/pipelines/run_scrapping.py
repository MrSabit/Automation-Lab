from pathlib import Path
import yaml
import csv
import sys

# add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scrapers.steam_scraper import SteamScraper
from config.settings import RAW_DATA_PATH, PROCESSED_DATA_PATH

def run():
    steam_scraper = SteamScraper()
    games = steam_scraper.scrape(pages=1)
    with open(RAW_DATA_PATH / "game_info.csv", "w", encoding="utf-8") as file:
        info_writer = csv.writer(file)
        info_writer.writerow(["game_id","title", "url", "price", "discount", "rating"])

        for game in games:
            info_writer.writerow([game["game_id"],game["title"], game["url"], game["price"], game["discount"], game["rating"]])

    with open(RAW_DATA_PATH / "game_detail.csv", "w", encoding="utf-8") as file:
        detail_writer = csv.writer(file)
        detail_writer.writerow(["game_id",
                                "developer", 
                                "publisher", 
                                "release_date", 
                                "genres", 
                                "desciption", 
                                "total_reviews", 
                                "positive_reviews", 
                                "negative_reviews", 
                                "current_players",
                                "rating"
                                ])

        for game in games:
            detail_writer.writerow([game["game_id"],
                                    game["developer"], 
                                    game["publisher"], 
                                    game["release_date"], 
                                    game["genres"], 
                                    game["description"],
                                    game["total_reviews"],
                                    game["positive_reviews"],
                                    game["negative_reviews"],
                                    game["current_players"],
                                    game["rating"]])
            


if __name__ == "__main__":
    run()