import database.models as api
from database.db_utils import getSession


def createGame(gameInfo: dict) -> dict:
    with getSession() as session:
        #Check if team already exists
        existingGame = session.query(api.Game).filter_by(game_id=gameInfo['game_id']).first()
        if existingGame:
            return {"Error": "Game {} already exists in the database.".format(gameInfo['game_id'])}
        #Create Team Object
        newTeam = api.Game(**gameInfo)
        #Add Team to Database
        try:
            session.add(newTeam)
            session.commit()
            return {'Success': "Team {} added Successfully".format(gameInfo['game_id'])}
        except Exception as e:
            session.rollback()
            print(e)
            return {'Error': "Error adding Team {}".format(gameInfo['game_id'])}
