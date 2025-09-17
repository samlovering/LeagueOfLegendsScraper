import pandas as pd
from database import player_db, team_db, asset_db, game_db
import unicodedata
from utils.app_state import AppState

'''
Helper Functions
Used around the match_scraper
'''

#Dataframe Helper function to clean up data with null checking
def get_value(df, column,index=0,default=None, transform_func=None):
    value = df[column].iloc[index] if not df[column].isnull().iloc[index] else default
    if transform_func and value is not None:
        value = transform_func(value)
    return value

'''
Draft Information
'''
def createTeamDraft(teamdf: pd.DataFrame) -> dict:
    return {
        'team_id': teamdf['teamid'][8:],
        'game_id': teamdf['gameid'],
        'ban1': asset_db.getChampionByName(teamdf['ban1'])['champion_id'],
        'ban2': asset_db.getChampionByName(teamdf['ban2'])['champion_id'],
        'ban3': asset_db.getChampionByName(teamdf['ban3'])['champion_id'],
        'ban4': asset_db.getChampionByName(teamdf['ban4'])['champion_id'],
        'ban5': asset_db.getChampionByName(teamdf['ban5'])['champion_id'],
        'pick1': asset_db.getChampionByName(teamdf['pick1'])['champion_id'],
        'pick2': asset_db.getChampionByName(teamdf['pick2'])['champion_id'],
        'pick3': asset_db.getChampionByName(teamdf['pick3'])['champion_id'],
        'pick4': asset_db.getChampionByName(teamdf['pick4'])['champion_id'],
        'pick5': asset_db.getChampionByName(teamdf['pick5'])['champion_id'],
    }

'''
Team Information
'''
# Helper function to safely get values from the DataFrame
def safe_get_value(df, column, default=None):
    if column in df and not pd.isna(df[column]):
        return df[column]
    return default


def createTeamGame(teamdf: pd.DataFrame) -> dict:
    # Query for team first
    if 'teamid' not in teamdf or pd.isna(teamdf['teamid']):
        return {'Error':'Team ID does not exist'}
    team_id = teamdf['teamid'][8:]
    team_query = team_db.getTeamById(team_id)
    
    # If Team does not exist, create with basic information
    if team_query.get('Error'):
        team_db.createTeam({
            'team_id': team_id,
            'team_name': teamdf['teamname'],
            'league': teamdf['league']
        })
        
    # Create Team Game
    team_game_dict = {
        # General Information
        'game_id': safe_get_value(teamdf, 'gameid'),
        'team_id': team_id,
        'game_length': int(safe_get_value(teamdf, 'gamelength', default=0)),
        'side': safe_get_value(teamdf, 'side', default=''),
        'result': bool(safe_get_value(teamdf, 'result', default=False)),
    }

    # Kill Stats
    team_combat = {
        'game_id': safe_get_value(teamdf, 'gameid'),
        'team_id': team_id,
        'kills': int(safe_get_value(teamdf, 'kills', default=0)),
        'deaths': int(safe_get_value(teamdf, 'deaths', default=0)),
        'assists': int(safe_get_value(teamdf, 'assists', default=0)),
        'doublekills': int(safe_get_value(teamdf, 'doublekills', default=0)),
        'triplekills': int(safe_get_value(teamdf, 'triplekills', default=0)),
        'quadrakills': int(safe_get_value(teamdf, 'quadrakills', default=0)),
        'pentakills': int(safe_get_value(teamdf, 'pentakills', default=0)),
        'firstblood': bool(safe_get_value(teamdf, 'firstblood', default=False)),
        'damagetochampions': int(safe_get_value(teamdf, 'damagetochampions', default=0))
    }

    # Objective Stats
    team_game_objectives = {
        'game_id': safe_get_value(teamdf, 'gameid'),
        'team_id': team_id,
        # Dragons
        'dragons': int(safe_get_value(teamdf, 'dragons', default=0)),
        'firstdragon': bool(safe_get_value(teamdf, 'firstdragon', default=False)),
        'infernals': int(safe_get_value(teamdf, 'infernals', default=0)),
        'mountains': int(safe_get_value(teamdf, 'mountains', default=0)),
        'clouds': int(safe_get_value(teamdf, 'clouds', default=0)),
        'oceans': int(safe_get_value(teamdf, 'oceans', default=0)),
        'chemtechs': int(safe_get_value(teamdf, 'chemtechs', default=0)),
        'hextechs': int(safe_get_value(teamdf, 'hextechs', default=0)),
        'elders': int(safe_get_value(teamdf, 'elders', default=0)),
        # Other Objectives
        'heralds': int(safe_get_value(teamdf, 'heralds', default=0)),
        'firstherald': bool(safe_get_value(teamdf, 'firstherald', default=False)),
        'voidgrubs': int(safe_get_value(teamdf, 'void_grubs', default=0)),
        'barons': int(safe_get_value(teamdf, 'barons', default=0)),
        'firstbaron': bool(safe_get_value(teamdf, 'firstbaron', default=False)),
        'atakhan': int(safe_get_value(teamdf,'atakhans',default=0)),
        # Towers
        'firsttower': bool(safe_get_value(teamdf, 'firsttower', default=False)),
        'firstmidtower': bool(safe_get_value(teamdf, 'firstmidtower', default=False)),
        'firsttothreetowers': bool(safe_get_value(teamdf, 'firsttothreetowers', default=False)),
        'towers': int(safe_get_value(teamdf, 'towers', default=0)),
        'turretplates': int(safe_get_value(teamdf, 'turretplates', default=0)),
        'inhibitors': int(safe_get_value(teamdf, 'inhibitors', default=0)),
    }

    # Economy Stats
    team_game_economy = {
        'game_id': safe_get_value(teamdf, 'gameid'),
        'team_id': team_id,
        'totalgold': int(safe_get_value(teamdf, 'totalgold', default=0)),
        'goldspent': int(safe_get_value(teamdf, 'goldspent', default=0)),
        'minionkills': int(safe_get_value(teamdf, 'minionkills', default=0)),
        'monsterkills': int(safe_get_value(teamdf, 'monsterkills', default=0)),
    }

    # Vision Stats
    team_game_vision = {
        'game_id': safe_get_value(teamdf, 'gameid'),
        'team_id': team_id,
        'wardsplaced': int(safe_get_value(teamdf, 'wardsplaced', default=0)),
        'wardskilled': int(safe_get_value(teamdf, 'wardskilled', default=0)),
        'controlwardsbought': int(safe_get_value(teamdf, 'controlwardsbought', default=0)),
        'visionscore': int(safe_get_value(teamdf, 'visionscore', default=0)),
    }

    # Stats at 15 Minutes
    team_game_at15 = {
        'game_id': safe_get_value(teamdf, 'gameid'),
        'team_id': team_id,
        'goldat15': int(safe_get_value(teamdf, 'goldat15', default=0)),
        'xpat15': int(safe_get_value(teamdf, 'xpat15', default=0)),
        'csat15': int(safe_get_value(teamdf, 'csat15', default=0)),
        'xpdiffat15': int(safe_get_value(teamdf, 'xpdiffat15', default=0)),
        'golddiffat15': int(safe_get_value(teamdf, 'golddiffat15', default=0)),
        'csdiffat15': int(safe_get_value(teamdf, 'csdiffat15', default=0)),
    }

    # Combine all dictionaries into a nested dictionary
    team_game = {
        'game_id': safe_get_value(teamdf, 'gameid'),
        'team_id': team_id,
        'team_game': team_game_dict,
        'team_game_combat': team_combat,
        'team_game_objectives': team_game_objectives,
        'team_game_economy': team_game_economy,
        'team_game_vision': team_game_vision,
        'team_game_at15': team_game_at15,
    }

    return team_game

    
'''
Player information

'''    
def createGamePlayer(playerdf: pd.DataFrame) -> dict:
    #Query for Player first
    player_id = playerdf['playerid'][10:]
    player_query = player_db.getPlayerById(player_id)
    if player_query.get('Error'):
        player_db.createPlayer({
            'player_id': player_id,
            'player_name': playerdf['playername'],
        })
    #Create Player Game
    player_game_dict = {
        'game_id': safe_get_value(playerdf, 'gameid'),
        'player_id': player_id,
        'team_id': safe_get_value(playerdf, 'teamid')[8:],
        'game_length': int(safe_get_value(playerdf, 'gamelength', default=0)),
        'side': safe_get_value(playerdf, 'side', default=''),
        'result': bool(safe_get_value(playerdf, 'result', default=False)),
        'champion_id': asset_db.getChampionByName(playerdf['champion'])['champion_id'],
    }
    player_game_combat = {
        'game_id': safe_get_value(playerdf, 'gameid'),
        'player_id': player_id,
        # Kill Stats
        'kills': int(safe_get_value(playerdf, 'kills', default=0)),
        'deaths': int(safe_get_value(playerdf, 'deaths', default=0)),
        'assists': int(safe_get_value(playerdf, 'assists', default=0)),
        'doublekills': int(safe_get_value(playerdf, 'doublekills', default=0)),
        'triplekills': int(safe_get_value(playerdf, 'triplekills', default=0)),
        'quadrakills': int(safe_get_value(playerdf, 'quadrakills', default=0)),
        'pentakills': int(safe_get_value(playerdf, 'pentakills', default=0)),
        # First Blood
        'firstblood': bool(safe_get_value(playerdf, 'firstblood', default=False)),
        'firstbloodkill': bool(safe_get_value(playerdf, 'firstbloodkill', default=False)),
        'firstbloodassist': bool(safe_get_value(playerdf, 'firstbloodassist', default=False)),
        'firstbloodvictim': bool(safe_get_value(playerdf, 'firstbloodvictim', default=False)),
        'damagetochampions': int(safe_get_value(playerdf, 'damagetochampions', default=0))
    }
    player_game_economy = {
        'game_id': playerdf['gameid'],
        'player_id': player_id,
        'totalgold': int(safe_get_value(playerdf,'totalgold',default=0)),
        'goldspent': int(safe_get_value(playerdf, 'goldspent', default=0)),
        'minionkills': int(safe_get_value(playerdf, 'minionkills', default=0)),
        'monsterkills': int(safe_get_value(playerdf, 'monsterkills', default=0)),
    }
    player_game_vision = {
        'game_id': playerdf['gameid'],
        'player_id': player_id,
        'wardsplaced': int(safe_get_value(playerdf, 'wardsplaced', default=0)),
        'wardskilled': int(safe_get_value(playerdf, 'wardskilled', default=0)),
        'controlwardsbought': int(safe_get_value(playerdf, 'controlwardsbought', default=0)),
        'visionscore': int(safe_get_value(playerdf, 'visionscore', default=0)),
    }
    player_game_at15 = {
        'game_id': playerdf['gameid'],
        'player_id': player_id,
        'goldat15': int(safe_get_value(playerdf, 'goldat15', default=0)),
        'xpat15': int(safe_get_value(playerdf, 'xpat15', default=0)),
        'csat15': int(safe_get_value(playerdf, 'csat15', default=0)),
        'xpdiffat15': int(safe_get_value(playerdf, 'xpdiffat15', default=0)),
        'golddiffat15': int(safe_get_value(playerdf, 'golddiffat15', default=0)),
        'csdiffat15': int(safe_get_value(playerdf, 'csdiffat15', default=0)),
    }
    gamePlayer = {
        'game_id': safe_get_value(playerdf, 'gameid'),
        'player_id': player_id,
        'game_player': player_game_dict,
        'game_player_combat': player_game_combat,
        'game_player_economy': player_game_economy,
        'game_player_vision': player_game_vision,
        'game_player_at15': player_game_at15,
    }
    return gamePlayer

'''
General Game Information
This is the basic identifiers for a game.
'''

def createGame(gamedf: pd.DataFrame) -> dict:
    game = {
    'game_id': get_value(gamedf, 'gameid'),
    'team1_id': get_value(gamedf[gamedf['side'] == 'Blue'], 'teamid', transform_func=lambda x: x[8:]),
    'team2_id': get_value(gamedf[gamedf['side'] == 'Red'], 'teamid', transform_func=lambda x: x[8:]),
    'date': get_value(gamedf, 'date'),
    'data_complete': get_value(gamedf, 'datacompleteness'),
    'url': get_value(gamedf, 'url'),
    'league': get_value(gamedf, 'league'),
    'year': str(get_value(gamedf, 'year')),
    'split': get_value(gamedf, 'split'),
    'playoffs': bool(get_value(gamedf, 'playoffs')),
    'game_in_series': int(get_value(gamedf, 'game')),
    'patch': str(get_value(gamedf, 'patch', transform_func=lambda x: str(x).replace("25", "15") if "25" in str(x) else str(x))),
    }
    return(game)
'''
Team + Player Creation
This takes dataframe data and ensures a team exists prior to creating game_data for them.
'''
def normalize_name(name):
        return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    
def createTeam(teamrow: pd.DataFrame):
    team_name = normalize_name(teamrow['teamname'])
    message = team_db.createTeam({
            'team_id': teamrow['teamid'][8:],
            'team_name': team_name,
            'league': teamrow['league']
        })
    return message

def createPlayer(playerrow: pd.DataFrame):
    message = player_db.createPlayer({
            'player_id': playerrow['playerid'][10:],
            'player_name': playerrow['playername'],
    })
    return message

def createTeamPlayer(playerrow: pd.DataFrame):
    message = player_db.createTeamPlayer({
            'team_id': playerrow['teamid'][8:],
            'player_id': playerrow['playerid'][10:],
            'role': playerrow['position']
            })
    return message


'''
Main Parser Controller
'''

# Hardcoded Major Leagues for now. (TODO:get the minor regions too)
major_leagues = ['LCK', 'LEC', 'LTA N', 'LTA S', 'LCP', 'LPL'] 
def parseCSV(file_path: str):
    df = pd.read_csv(file_path)
    groupedGames = df.groupby('gameid')
    for game_id, game_data in groupedGames:
        #Only filter for major regions.
        if game_data['league'].isin(major_leagues).any():
            # Attempt to create players and teams
            # Get rows where there is no playerid or playername (team rows)
            team_rows = game_data[game_data['playerid'].isnull() & game_data['playername'].isnull()]
            
            #Create teams if they do not exist
            for _, team_data in team_rows.iterrows():
                #Skip if no team id
                if pd.isna(team_data['teamid']):
                    AppState.logger.warning('Team does not have ID, skipping team creation: {}'.format(team_data))
                    continue
                # Create team if it doesn't exist
                createTeam(team_data)
            
            # Get rows where there is playerid and playername (player rows)
            player_rows = game_data[game_data['playerid'].notnull() & game_data['playername'].notnull()]
            
            for _, player_data in player_rows.iterrows():
                #skip if no team id
                if pd.isna(player_data['teamid']):
                    AppState.logger.warning('Player does not have a team. Skipping player creation: {}'.format(player_data))
                    continue
                # Create player if it doesn't exist
                createPlayer(player_data)
                createTeamPlayer(player_data)
            
            # Check if any team is 'unknown team' or if teamid is missing
            if any(team_data['teamname'] == 'unknown team' or pd.isna(team_data['teamid']) for _, team_data in team_rows.iterrows()):
                continue

            # Begin by creating game:
            gameDict = createGame(game_data)
            game_db.createGame(gameDict)
            
            for _, team_data in team_rows.iterrows():
                team_game = createTeamGame(team_data)
                if team_game.get('Error'):
                    AppState.logger.warning('Team data does not exist. Skipping team game creation: {}'.format(team_game))
                    continue
                else:
                    team_db.insertTeamGame(team_game)
                    team_draft = createTeamDraft(team_data)
                    team_db.insertTeamDraft(team_draft)
                    
            for _, player_data in player_rows.iterrows():
                game_player = createGamePlayer(player_data)
                player_db.insertGamePlayer(game_player)