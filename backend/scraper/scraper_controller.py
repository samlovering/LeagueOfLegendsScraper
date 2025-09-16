from scraper.web_connections import oracle_elixir
from scraper.match_scraper import match_scraper

def run_scaper():
    #Unsure if I need to rebuild tables or not.
    file_path = oracle_elixir.downloadFromGoogleDrive()
    match_scraper.parseCSV(file_path)