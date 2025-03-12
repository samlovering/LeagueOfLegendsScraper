from typing import List
from sqlalchemy import func
import database.models as api
from database.db_utils import getSession
from thefuzz import fuzz


def getAllTeamNames() -> List[dict]:
    with getSession() as session:
        teams = session.query(api.Team.team_name,api.Team.team_id).all()
        return teams

def createTeam(teamInfo: dict) -> dict:
    with getSession() as session:
        #Check if team already exists
        existingTeam = session.query(api.Team).filter_by(team_id=teamInfo['team_id']).first()
        if existingTeam:
            return {"Error": "Team {} already exists in the database.".format(teamInfo['team_id'])}
        #Create Team Object
        newTeam = api.Team(
            team_id=teamInfo['team_id'],
            team_name=teamInfo['team_name'],
            league=teamInfo['league'],
        )
        #Add Team to Database
        try:
            session.add(newTeam)
            session.commit()
            return {'Success': "Team {} added Successfully".format(teamInfo['team_name'])}
        except Exception as e:
            session.rollback()
            return {'Error': "Error adding Team {}".format(teamInfo['team_name'])}

'''
Team Getter Methods
'''

def getTeamById(id: str) -> dict:
    with getSession() as session:
        team = session.query(api.Team).filter_by(team_id=id).first()
        if team:
            return {
                'team_id': team.team_id,
                'team_name': team.team_name,
                'league':team.league,
            }
        else:
            return {"Error": "Team not found. ID:{}".format(id)}


def getTeamsByLeague(league_name: str) -> List:
    with getSession() as session:
        teams = session.query(
            api.Team,
        ).join(
            api.Game, (api.Game.team1_id == api.Team.team_id) | (api.Game.team2_id == api.Team.team_id)
        ).filter(
            api.Game.league == league_name
        ).all()
        teamList = []
        if teams:
            for team in teams:
                teamList.append({
                    'team_id': team.team_id,
                    'team_name':team.team_name
                })
            return teamList
        else:
            return {"Error": "League not found. League:{}".format(league_name)}


'''
Team Getter with Fuzzy Matching

'''
def getTeamBySimilarName(team_name: str) -> dict:
    best_match = None
    best_score = 0
    teams = getAllTeamNames()
    for team in teams:
        score = fuzz.ratio(team_name, team.team_name)
        if score > best_score:
            print('New Best Match: ', team.team_name, score)
            best_score = score
            best_match = team
    if best_match:
        return {
            'team_id': best_match.team_id,
            'team_name': best_match.team_name,
        }
    else:
        return {"Error": "Team not found. Team Name: {}".format(team_name)}

'''

Team Game Getter Functions

'''

def getTeamGames(teamId: str):
    with getSession() as session:
        team_games = session.query(
            api.Team_Game,
            api.Team_Game_Combat,
            api.Team_Game_Objectives,
            api.Team_Game_Economy,
            api.Team_Game_Vision,
            api.Team_Game_At15
        ).filter(
            api.Team_Game.team_id == teamId,
            api.Team_Game.team_game_id == api.Team_Game_Combat.team_game_id,
            api.Team_Game.team_game_id == api.Team_Game_Objectives.team_game_id,
            api.Team_Game.team_game_id == api.Team_Game_Economy.team_game_id,
            api.Team_Game.team_game_id == api.Team_Game_Vision.team_game_id,
            api.Team_Game.team_game_id == api.Team_Game_At15.team_game_id
        ).all()
        
        organized_team_games = {}
        for game in team_games:
            team_game_id = game.Team_Game.team_game_id
            organized_team_games[team_game_id] = {
            'team_game': {
                'team_id': game.Team_Game.team_id,
                'game_id': game.Team_Game.game_id,
                'result': game.Team_Game.result,
                'game_length': game.Team_Game.game_length,
                'side': game.Team_Game.side
            },
            'team_game_combat': {
                'kills': game.Team_Game_Combat.kills,
                'deaths': game.Team_Game_Combat.deaths,
                'assists': game.Team_Game_Combat.assists,
                'firstblood': game.Team_Game_Combat.firstblood,
            },
            'team_game_objectives': {
                'firstdragon': game.Team_Game_Objectives.firstdragon,
                'firstherald':game.Team_Game_Objectives.firstherald,
                'firsttower':game.Team_Game_Objectives.firsttower,
                'firstbaron':game.Team_Game_Objectives.firstbaron, 
                'turretplates':game.Team_Game_Objectives.turretplates,
                'towers':game.Team_Game_Objectives.towers,
                'inhibitors':game.Team_Game_Objectives.inhibitors,
                'dragons':game.Team_Game_Objectives.dragons,
                'voidgrubs':game.Team_Game_Objectives.voidgrubs,
                'barons':game.Team_Game_Objectives.barons,
                'heralds':game.Team_Game_Objectives.heralds,
            },
            'team_game_economy': {
                'totalgold': game.Team_Game_Economy.totalgold,
                'goldspent': game.Team_Game_Economy.goldspent,
                'minionkills': game.Team_Game_Economy.minionkills,
                'monsterkills':game.Team_Game_Economy.monsterkills,
            },
            'team_game_vision': {
                'wardsplaced': game.Team_Game_Vision.wardsplaced,
                'wardskilled': game.Team_Game_Vision.wardskilled,
                'visionscore': game.Team_Game_Vision.visionscore,
                'controlwardsbought': game.Team_Game_Vision.controlwardsbought,
            },
            'team_game_at15': {
                'golddiffat15': game.Team_Game_At15.golddiffat15,
                'xpdiffat15': game.Team_Game_At15.xpdiffat15,
                'csdiffat15': game.Team_Game_At15.csdiffat15,
                'goldat15':game.Team_Game_At15.goldat15,
                'xpat15':game.Team_Game_At15.xpat15,
                'csat15':game.Team_Game_At15.csat15,
            }
            }
        
        return organized_team_games
    
#getCombinedTeamGames returns the total counts of stats in games.
#This includes the opponents teams, mostly used for kill/dragon over/unders.
def getCombinedTeamGames(teamId: str):
    with getSession() as session:
        game_ids = session.query(
            api.Team_Game.game_id
        ).filter(
            api.Team_Game.team_id == teamId
        ).distinct()
        
        combined_stats = session.query(
            api.Team_Game.game_id,  # Group by game_id
            func.sum(api.Team_Game_Combat.kills).label('total_kills'),  # Sum kills
            func.sum(api.Team_Game_Economy.totalgold).label('total_gold'),  # Sum gold
            func.sum(api.Team_Game_Objectives.dragons).label('total_dragons'),  # Sum dragons
            func.sum(api.Team_Game_Objectives.towers).label('total_towers'),  # Sum towers
            func.sum(api.Team_Game_Objectives.barons).label('total_barons'),  # Sum barons
            func.sum(api.Team_Game_Objectives.inhibitors).label('total_inhibitors')  # Sum inhibitors
        ).join(
            api.Team_Game_Combat, api.Team_Game.team_game_id  == api.Team_Game_Combat.team_game_id 
        ).join(
            api.Team_Game_Economy, api.Team_Game.team_game_id  == api.Team_Game_Economy.team_game_id 
        ).join(
            api.Team_Game_Objectives, api.Team_Game.team_game_id  == api.Team_Game_Objectives.team_game_id 
        ).filter(
           api.Team_Game.game_id.in_(game_ids)
        ).group_by(
            api.Team_Game.game_id  # Group by game_id to aggregate stats per game
        ).all()
        
        combined_team_games = []
        for stat in combined_stats:
            combined_team_games.append({
                'game_id': stat.game_id,
                'total_kills': stat.total_kills,
                'total_gold': stat.total_gold,
                'total_dragons': stat.total_dragons,
                'total_towers': stat.total_towers,
                'total_barons': stat.total_barons,
                'total_inhibitors': stat.total_inhibitors
            })
        return combined_team_games
        
               
'''

Scraper Insert Funciton

'''

def insertTeamGame(teamGame: dict) -> dict:
    with getSession() as session:
        #Create team_game_id
        team_game_id = teamGame['game_id']+teamGame['team_id']
        #First check for existing teamGame
        existingTeamGame = session.query(api.Team_Game).filter(api.Team_Game.team_game_id==team_game_id).first()
        if existingTeamGame:
            return {"Error": "Team Game {} already exists in the database.".format(team_game_id)}
        #Create Team Game objects
        team_game = api.Team_Game(team_game_id=team_game_id, **teamGame['team_game'])
        team_game_combat = api.Team_Game_Combat(team_game_id=team_game_id, **teamGame['team_game_combat'])
        team_game_objectives = api.Team_Game_Objectives(team_game_id=team_game_id, **teamGame['team_game_objectives'])
        team_game_economy = api.Team_Game_Economy(team_game_id=team_game_id, **teamGame['team_game_economy'])
        team_game_vision = api.Team_Game_Vision(team_game_id=team_game_id, **teamGame['team_game_vision'])
        team_game_at15 = api.Team_Game_At15(team_game_id=team_game_id, **teamGame['team_game_at15'])
        try:
            session.add(team_game)
            session.add(team_game_combat)
            session.add(team_game_objectives)
            session.add(team_game_economy)
            session.add(team_game_vision)
            session.add(team_game_at15)
            session.commit()
            return {'Success': 'Team Game {} added successfully'.format(team_game_id)}
        except Exception as e:
            session.rollback()
            print(e)
            return {"Error": "Error adding Team Game. ID:{}".format(team_game_id)}
        
#Team Draft Insertion

def insertTeamDraft(teamDraft: dict) -> dict:
    with getSession() as session:
        team_game_id = teamDraft['game_id']+teamDraft['team_id']
        #check for existing draft
        existingTeamDraft = session.query(api.Team_Draft).filter(api.Team_Draft.team_game_id==team_game_id).first()
        if existingTeamDraft:
            return {"Error": "Team Draft {} already exists in the database.".format(team_game_id)}
        #Create draft object
        team_draft = api.Team_Draft(team_game_id=team_game_id, **teamDraft)
        #attempt to insert
        try:
            session.add(team_draft)
            session.commit()
            return {'Success': 'Team Draft {} added successfully'.format(team_game_id)}
        except Exception as e:
            session.rollback()
            print(e)
            return {"Error": "Error adding Team Draft. ID:{}".format(team_game_id)}
        