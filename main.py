import datetime
from scraper.asset_scraper import *
from scraper.asset_scraper import champion_scraper
from scraper.match_scraper import match_scraper
from scraper.schedule_scraper import schedule_scraper
from database import db_utils,asset_db,team_db,game_db,lolesports_db
from stat_calc import betting_stats,champion_stats
from scraper import scraper_controller
from flask_server import app

if __name__ == "__main__":
   #Run Scraper For most receent data
   #scraper_controller.run_scaper()
   #Get Betting stats for Gen.G
   #app.start_server()
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
   #lolesports_db.get_unique_leagues()
   games =schedule_scraper.get_upcomming_matches(end_date=(datetime.datetime.now()+datetime.timedelta(days=1)))
   for game in games:
      for game_team in game['match']['teams']:
         print(game_team['name'])
         db_team = team_db.getTeamBySimilarName(game_team['name'])
         print(db_team)
