import database.models as api
from database.db_utils import getSession


def createPlayer(playerInfo: dict) -> dict:
    with getSession() as session:
        #Check if team already exists
        existingTeam = session.query(api.Player).filter_by(player_id=playerInfo['player_id']).first()
        if existingTeam:
            return {"Error": "Player {} already exists in the database.".format(playerInfo['player_id'])}
        #Create Team Object
        newPlayer = api.Player(
            player_id=playerInfo['player_id'],
            player_name=playerInfo['player_name'],
        )
        #Add Team to Database
        try:
            session.add(newPlayer)
            session.commit()
            return {'Success': "Player {} added Successfully".format(playerInfo['player_name'])}
        except Exception as e:
            session.rollback()
            print(e)

def getPlayerById(id: str) -> dict:
    with getSession() as session:
        player = session.query(api.Player).filter_by(player_id=id).first()
        if player:
            return {
                'player_id':player.player_id,
                'player_name':player.player_name,
            }
        else:
            return {"Error": "Player not found. ID:{}".format(id)}
        

def insertGamePlayer(gamePlayer: dict) -> dict:
    with getSession() as session:
        #Create player_game_id
        game_player_id = gamePlayer['game_id'] + gamePlayer['player_id']
        #check for existing gamePlayer
        existingGamePlayer  = session.query(api.Game_Player).filter(api.Game_Player.game_player_id==game_player_id).first
        if existingGamePlayer:
            return {"Error":"Game Player {} already exists in database".format(game_player_id)}
        
        game_player = api.Game_Player(game_player_id=game_player_id, **gamePlayer['game_player'])
        game_player_combat = api.Game_Player_Combat(game_player_id=game_player_id, **gamePlayer['game_player_combat'])
        game_player_economy = api.Game_Player_Economy(game_player_id=game_player_id,**gamePlayer['game_player_economy'])
        game_player_vision = api.Game_Player_Vision(game_player_id=game_player_id,**gamePlayer['game_player_vision'])
        game_player_at15 = api.Game_Player_At15(game_player_id=game_player_id,**gamePlayer['game_player_at15'])
        try:
            session.add(game_player)
            session.add(game_player_combat)
            session.add(game_player_economy)
            session.add(game_player_vision)
            session.add(game_player_at15)
            session.commit()
            return {'Success': 'Game Player {} added successfully'.format(game_player_id)}
        except Exception as e:
            session.rollback()
            print(e)
            return {"Error": "Error adding Game Player. ID:{}".format(game_player_id)}