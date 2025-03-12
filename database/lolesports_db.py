'''
Samuel Lovering
3/7/24

This is a database helper file to access lolesports_name data from the "leagues" tables. For usage in schedule.
'''

from typing import List
from database.db_utils import getSession
import database.models as api

'''
This returns a list of unique leagues from the game table of the database to build the lolesports_name db.
'''
def get_unique_leagues() -> List[str]:
    with getSession() as session:
        league_query = session.query(api.Game.league).distinct().all()
        unique_leagues = [league[0] for league in league_query]
        return unique_leagues
    
'''
This returns a league ID given a name.

'''
        
'''
This creates a db table with the league id, and the name of the league from oracleselixir
'''
def create_league_table() -> List[dict]:
    league_mapping = [
    {'league_id': '113464388705111224', 'oracle_name': 'FS', 'lolesports_name': 'First Stand'},
    {'league_id': '113470291645289904', 'oracle_name': 'LTA N', 'lolesports_name': 'LTA North'},
    {'league_id': '113475149040947852', 'oracle_name': 'LTA', 'lolesports_name': 'LTA Cross-Conference'},
    {'league_id': '113475181634818701', 'oracle_name': 'LTA S', 'lolesports_name': 'LTA South'},
    {'league_id': '98767991302996019', 'oracle_name': 'LEC', 'lolesports_name': 'LEC'},
    {'league_id': '98767991310872058', 'oracle_name': 'LCK', 'lolesports_name': 'LCK'},
    {'league_id': '98767991314006698', 'oracle_name': 'LPL', 'lolesports_name': 'LPL'},
    {'league_id': '113476371197627891', 'oracle_name': 'LCP', 'lolesports_name': 'LCP'},
    {'league_id': '109511549831443335', 'oracle_name': 'NACL', 'lolesports_name': 'NACL'},
    {'league_id': '100695891328981122', 'oracle_name': 'EM', 'lolesports_name': 'EMEA Masters'},
    {'league_id': '98767991349978712', 'oracle_name': 'LJL', 'lolesports_name': 'LJL'},
    {'league_id': '98767991343597634', 'oracle_name': 'TCL', 'lolesports_name': 'TCL'},
    {'league_id': '105266098308571975', 'oracle_name': 'NLC', 'lolesports_name': 'NLC'},
    {'league_id': '105266103462388553', 'oracle_name': 'LFL', 'lolesports_name': 'La Ligue Française'},
    {'league_id': '105266101075764040', 'oracle_name': 'LPLOL', 'lolesports_name': 'Liga Portuguesa'},
    {'league_id': '105266094998946936', 'oracle_name': 'LIT', 'lolesports_name': 'LoL Italian Tournament'},
    {'league_id': '113673877956508505', 'oracle_name': 'RL', 'lolesports_name': 'Rift Legends'},
    {'league_id': '105266074488398661', 'oracle_name': 'LVPSL', 'lolesports_name': 'SuperLiga'},
    {'league_id': '105266091639104326', 'oracle_name': 'PRM', 'lolesports_name': 'Prime League'},
    {'league_id': '105266106309666619', 'oracle_name': 'HM', 'lolesports_name': 'Hitpoint Masters'},
    {'league_id': '105266111679554379', 'oracle_name': 'EBL', 'lolesports_name': 'Esports Balkan League'},
    {'league_id': '105266108767593290', 'oracle_name': 'HLL', 'lolesports_name': 'Hellenic Legends League'},
    {'league_id': '109545772895506419', 'oracle_name': 'AL', 'lolesports_name': 'Arabian League'},
    {'league_id': '98767991335774713', 'oracle_name': 'LCKC', 'lolesports_name': 'LCK Challengers'},
    {'league_id': '105549980953490846', 'oracle_name': 'CD', 'lolesports_name': 'Circuito Desafiante'},
    {'league_id': '110371976858004491', 'oracle_name': 'LRN', 'lolesports_name': 'North Regional League'},
    {'league_id': '110372322609949919', 'oracle_name': 'LRS', 'lolesports_name': 'South Regional League'},
    {'league_id': '98767975604431411', 'oracle_name': 'Worlds', 'lolesports_name': 'Worlds'},
    {'league_id': '98767991325878492', 'oracle_name': 'MSI', 'lolesports_name': 'MSI'},
    ]
    with getSession() as session:
        try:
            session.bulk_insert_mappings(api.League, league_mapping)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            return {'Error': 'Leagues unable to be added'}