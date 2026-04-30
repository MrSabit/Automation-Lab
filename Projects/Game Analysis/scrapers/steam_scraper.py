import time
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from config.settings import STEAM_URL, STEAM_HEADERS, STEAM_DELAY
from scrapers.base_scraper import BaseScraper
import re

# =========================
# STEAM SCRAPER
# =========================
class SteamScraper(BaseScraper):

    def __init__(self):
        super().__init__(
            base_url=STEAM_URL,
            headers=STEAM_HEADERS,
            delay=STEAM_DELAY
        )
        print("[INIT] SteamScraper initialized")

    def scrape(self, pages=1):
        print(f"[START] Scraping started | pages={pages}")

        all_games = []

        for page in range(pages):
            print(f"\n[SEARCH] Fetching page {page}")

            html = self.fetch_search_page(page)

            if not html:
                print(f"[ERROR] Failed to fetch search page {page}")
                continue

            games = self.parse_search(html)

            print(f"[INFO] Found {len(games)} games on page {page}")

            for i, game in enumerate(games, start=1):

                print(f"[GAME] {i}/{len(games)} -> {game['title']}")

                if game["url"]:
                    print(f"[DETAIL] Fetching: {game['url']}")

                    detail_html = self.fetch_detail_page(game["url"])

                    if detail_html:
                        detail_data = self.parse_detail(detail_html, game["url"])
                        game.update(detail_data)
                        print(f"[OK] Detail added for {game['game_id']}")
                    else:
                        print(f"[WARN] No detail HTML for {game['title']}")

                all_games.append(game)

            print(f"[PAGE DONE] Page {page} completed")

        print(f"\n[DONE] Scraping finished | total games={len(all_games)}")

        return all_games

    # -------------------------
    # SEARCH PAGE
    # -------------------------
    def fetch_search_page(self, page):
        print(f"[HTTP] Requesting search page {page}")

        url = self.base_url
        params = {
            "query": "",
            "start": page * 25,
            "count": 25
        }

        res = self.get(url, params=params)

        if res:
            print("[HTTP] Success")
            return res.text

        print("[HTTP] Failed request")
        return None

    def parse_search(self, html):
        soup = BeautifulSoup(html, "html.parser")
        games = []

        for item in soup.select(".search_result_row"):

            url = item.get("href", None)
            game_id = self.extract_game_id(url)

            games.append({
                "game_id": game_id,
                "title": self._safe_text(item, ".title"),
                "url": url,
                "price": self._safe_text(item, ".discount_final_price"),
                "discount": self._safe_text(item, ".discount_pct", "0%"),
                "rating": self._safe_attr(item, ".search_review_summary", "data-tooltip-html")
            })

        return games

    # -------------------------
    # DETAIL PAGE
    # -------------------------
    def fetch_detail_page(self, url):
        print(f"[HTTP] Detail request -> {url}")

        res = self.get(url)

        if res:
            print("[HTTP] Detail success")
            return res.text

        print("[HTTP] Detail failed")
        return None

    def parse_detail(self, html, url):
        game_id = self.extract_game_id(url)
        soup = BeautifulSoup(html, "html.parser")

        # -----------------------------
        # Reviews extraction
        # -----------------------------
        review_data = self.extract_review_data(soup)

        # -----------------------------
        # Player stats (if available)
        # -----------------------------
        current_players = self.extract_current_players(soup)


        return {
            "game_id": game_id,
            "developer": self._extract_text_by_label(soup, "Developer:"),
            "publisher": self._extract_text_by_label(soup, "Publisher:"),
            "release_date": self._extract_release_date(soup),
            "genres": self._extract_genres(soup),
            "description": self._safe_text(soup, ".game_description_snippet"),
            "current_players": current_players,
            **review_data
        }
    def extract_rating(self, soup):
        try:
            tag = soup.select_one(".user_reviews_summary_row .game_review_summary")
            return tag.text.strip() if tag else None
        except:
            return None
    def extract_review_data(self, soup):
        total, positive, negative = self.extract_reviews(soup)
        rating = self.extract_rating(soup)
        return {
            "total_reviews": total,
            "positive_reviews": positive,
            "negative_reviews": negative,
            "rating": rating
        }
    def extract_reviews(self, soup):
        try:
            tag = soup.select_one(".user_reviews_summary_row")

            if not tag:
                return None, None, None

            tooltip = tag.get("data-tooltip-html", "")

            # Example inside tooltip:
            # "1,234,567 user reviews<br>95% positive"

            total_match = re.search(r"([\d,]+)\s+user reviews", tooltip)
            positive_match = re.search(r"(\d+)% positive", tooltip)

            total = int(total_match.group(1).replace(",", "")) if total_match else None
            positive_percent = int(positive_match.group(1)) if positive_match else None

            if total and positive_percent is not None:
                positive = int(total * (positive_percent / 100))
                negative = total - positive
            else:
                positive, negative = None, None

            return total, positive, negative

        except:
            return None, None, None
    def extract_current_players(self, soup):
        try:
            tag = soup.select_one(".game_area_play_stats")

            if not tag:
                return None

            text = tag.text.strip()

            match = re.search(r"([\d,]+)", text)

            return int(match.group(1).replace(",", "")) if match else None

        except:
            return None
        # -------------------------
        # FIXED METHOD (IMPORTANT)
        # -------------------------
    def extract_game_id(self, url):
        try:
            return url.split("/app/")[1].split("/")[0]
        except:
            return None

    # -------------------------
    # HELPERS
    # -------------------------
    def _safe_text(self, parent, selector, default=None):
        tag = parent.select_one(selector)
        return tag.text.strip() if tag else default

    def _safe_attr(self, parent, selector, attr, default=None):
        tag = parent.select_one(selector)
        return tag.get(attr) if tag and tag.get(attr) else default

    def _extract_text_by_label(self, soup, label):
        try:
            block = soup.find(string=label)
            if not block:
                return None
            return block.find_next().text.strip()
        except:
            return None

    def _extract_release_date(self, soup):
        return self._safe_text(soup, ".date")

    def _extract_genres(self, soup):
        genres = soup.select(".app_tag")
        return [g.text.strip() for g in genres] if genres else []


# =========================
# RUN EXAMPLE
# =========================
if __name__ == "__main__":
    scraper = SteamScraper()

    data = scraper.scrape(pages=1)

    print("\nSAMPLE OUTPUT:")
    for game in data[:3]:
        print(game)