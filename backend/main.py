import threading

import sqlalchemy
from scraper.asset_scraper import *
from scraper.asset_scraper import champion_scraper
from database import db_utils,asset_db
from scraper import scraper_controller
from flask_server import app
from utils import log_manager
from utils.app_state import AppState


def run():
   """This starts the scraper in a new thread, attaches a logger, and starts the server.
   """
   complete = db_utils.buildTables()
   while complete == False:
      pass
   
   # Initialize the logger
   AppState.logger = log_manager.LogManager().get_logger()
   AppState.logger.info("Logger initialized.")
   
   #Create the champion table if it doesn't exist
   AppState.logger.info("Building champion database.")
   champion_list = champion_scraper.createChampionList()
   asset_db.createChampionDatabase(champion_list)
   
   # Start the scraper in a new thread
   #TODO: put this in a scheduler.
   AppState.logger.info("Starting scraper.")
   scraper_thread = threading.Thread(target=scraper_controller.run_scaper)
   scraper_thread.start()
   
   # Start the Flask server.
   app.start_server()

if __name__ == "__main__":
   #Run Scraper For most receent data
   run()
   #scraper_controller.run_scaper()
   #Get Betting stats for Gen.G
   # app.start_server()
   # teams = team_db.getTeamsByLeague('LCK')
   # print(teams)
   # for team in teams:
   #    print(betting_stats.create_team_betting_stats(team['team_id']))
   # print("\n\nLPL Synergies")
   # lpl = champion_stats.getSynergies(league='LPL',patch='25.04',minGames=1)
   # for syn in lpl:
   #    print(syn)
   # print("\n\nGen.G Synergies")
   # geng = champion_stats.getSynergies(teamId='50f58982d91a36557ec8aec52ab014f')
   # for syn in geng[:10]:
   #    print(syn)
   # print('\n\nPatch 15.3 Synergies')
   # patch = champion_stats.getSynergies(minGames=10, patch='15.03')
   # for syn in patch:
   #    print(syn)
   # print("\n\nGlobal Synergies")
   # globe = champion_stats.getSynergies(minGames=20)
   # for syn in globe[:30]:
   #    print(syn)
   # print('Gen.G Meta Read')
   # champion_stats.create_team_meta_page(teamId='50f58982d91a36557ec8aec52ab014f')
   # topLeagues = ['LCK','LTA N','LTA S','LPL', 'LCP']
   # patches = []
   # champion_stats.create_global_meta_page(league=topLeagues)
   # lolesports_db.get_unique_leagues()
   
   # #Predict Kills Test
   # over_under = [19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5,32.5,33.5,34.5]
   # over_under2 = range(19,35)
   # #predict_kills.getPredictionData('8eb884e168f28402ce685bedebb5250','3a1d18f46bcb3716ebcfcf4ef068934')
   # predict_kills.createPoissonKillEstimates('75760dca486d4682426196b76bd1a54','3a1d18f46bcb3716ebcfcf4ef068934',over_under2)
   
   # #Upcomming Matches
   # games =schedule_scraper.get_upcomming_matches(end_date=(datetime.datetime.now()+datetime.timedelta(days=1)))
   # for game in games:
   #    team_ids = []
   #    for game_team in game['match']['teams']:
   #       if game_team['name'] != 'TBD':
   #          print(game_team['name'])
   #          db_team = team_db.getTeamBySimilarName(game_team['name'])
   #          if db_team:
   #             team_ids.append(db_team['team_id'])
   #             print(db_team)
   #    predict_kills.createPoissonKillEstimates(team_ids[0],team_ids[1],over_under)
   #    predict_kills.createNormalKillEstimates(team_ids[0],team_ids[1],over_under)
