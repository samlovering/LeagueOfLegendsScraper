from scraper.asset_scraper import *
from scraper.asset_scraper import champion_scraper
from scraper.match_scraper import match_scraper
from database import db_utils,asset_db

if __name__ == "__main__":
    db_utils.dropTables()
    db_utils.buildTables()
    champs = champion_scraper.createChampionList()
    asset_db.createChampionDatabase(champs)
    
    file_path = 'scraper/match_scraper/match_data.csv'
    match_scraper.parseCSV(file_path)