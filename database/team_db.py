import database.models as api
from database.db_utils import getSession


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

def insertTeamDraft(teamDraft: dict) -> dict:
    with getSession() as session:
        team_game_id = teamDraft['game_id']+teamDraft['team_id']
        team_draft = api.Team_Draft(team_game_id=team_game_id, **teamDraft)
        try:
            session.add(team_draft)
            session.commit()
            return {'Success': 'Team Draft {} added successfully'.format(team_game_id)}
        except Exception as e:
            session.rollback()
            print(e)
            return {"Error": "Error adding Team Draft. ID:{}".format(team_game_id)}

def insertTeamGame(teamGame: dict) -> dict:
    with getSession() as session:
        #Create team_game_id
        team_game_id = teamGame['game_id']+teamGame['team_id']
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
