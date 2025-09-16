import database.models as api
from database.db_utils import getSession
from utils.app_state import AppState
from sqlalchemy import func
from sqlalchemy.orm import aliased

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
            
def createTeamPlayer(playerInfo: dict) -> dict:
    """Create a link between a player and a team."""
    with getSession() as session:
        #Check if team_player already exists
        existingTeamPlayer = session.query(api.Team_Player).filter_by(player_id=playerInfo['player_id']).first()
        if existingTeamPlayer:
            return {"Error": "Team_Player {} already exists in the database.".format(playerInfo['player_id'])}
        #Create Team Object
        newTeamPlayer = api.Team_Player(
            team_player_id=playerInfo['team_id']+playerInfo['player_id'],
            team_id=playerInfo['team_id'],
            player_id=playerInfo['player_id'],
            role=playerInfo['role']
        )
        #Add Team to Database
        try:
            session.add(newTeamPlayer)
            session.commit()
            return {'Success': "Team_Player {} added Successfully".format(playerInfo['player_id'])}
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
        
def getBasicPlayerStats(playerId: str) -> dict:
    """Gets basic stats for a player id, used on team overview page."""
    with getSession() as session:
        # Get all games for the player
        combat_stats = (
            session.query(
            func.sum(api.Game_Player_Combat.kills).label('kills'),
            func.sum(api.Game_Player_Combat.assists).label('assists'),
            func.sum(api.Game_Player_Combat.deaths).label('deaths'),
            func.avg(api.Game_Player_Combat.damagetochampions).label('avg_damage_to_champions')
            )
            .filter(api.Game_Player_Combat.player_id == playerId)
        ).one()

        gold_stats = (
            session.query(
            func.avg(api.Game_Player_Economy.totalgold).label('avg_total_gold')
            )
            .filter(api.Game_Player_Economy.player_id == playerId)
        ).one()

        # Get list of champion_ids played
        champion_counts = (
            session.query(
            api.Game_Player.champion_id,
            api.Champion.champion_name,
            func.count(api.Game_Player.champion_id).label('count')
            )
            .join(api.Champion, api.Game_Player.champion_id == api.Champion.champion_id)
            .filter(api.Game_Player.player_id == playerId)
            .group_by(api.Game_Player.champion_id, api.Champion.champion_name)
            .all()
        )
        champion_list = [
            {"champion_id": row.champion_id, "champion_name": row.champion_name, "count": row.count}
            for row in champion_counts
        ]

        kills = combat_stats.kills or 0
        assists = combat_stats.assists or 0
        deaths = combat_stats.deaths or 1  # avoid division by zero
        kda = (kills + assists) / deaths if deaths else 0

        return {
            "kda": round(kda, 2),
            "avg_damage_to_champions": float(combat_stats.avg_damage_to_champions or 0),
            "champions_played": champion_list,
            "avg_total_gold": float(gold_stats.avg_total_gold or 0)
        }
        
def getPlayersByTeamId(teamId: str) -> list[dict]:
    """Gets a list of players for a given teamID"""
    with getSession() as session:
        # Join Team_Player with Player to get player_name
        players = (
            session.query(api.Team_Player, api.Player)
            .join(api.Player, api.Team_Player.player_id == api.Player.player_id)
            .filter(api.Team_Player.team_id == teamId)
            .all()
        )
        player_list = []
        if players:
            for team_player, player in players:
                player_list.append({
                    'player_id': team_player.player_id,
                    'player_name': player.player_name,
                    'role': team_player.role
                })
            return player_list
        else:
            return {"Error": "No players found for team ID:{}".format(teamId)}

def insertGamePlayer(gamePlayer: dict) -> dict:
    with getSession() as session:
        #Create player_game_id
        game_player_id = gamePlayer['game_id'] + gamePlayer['player_id']
        #check for existing gamePlayer
        existingGamePlayer  = session.query(api.Game_Player).filter(api.Game_Player.game_player_id==game_player_id).first()
        if existingGamePlayer:
            AppState.logger.info("Game Player {} already exists in database".format(game_player_id))
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
            AppState.logger.error("Error adding Game Player. ID:{}. Error:{}".format(game_player_id,e))
            return {"Error": "Error adding Game Player. ID:{}".format(game_player_id)}