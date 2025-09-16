from database import team_db



def create_team_betting_stats(teamId: str) -> dict:
    #Get team stats data
    teaminfo = team_db.getTeamById(teamId)
    teamGames = team_db.getTeamGames(teamId)
    combinedTeamGames = team_db.getCombinedTeamGames(teamId)
    #Create Team averages
    games_won = 0
    first_blood_games = 0
    first_herald_games = 0
    first_tower_games = 0
    first_dragon_games = 0
    first_baron_games = 0
    total_gold = 0
    total_kills=0
    total_deaths=0
    total_towers=0
    total_game_time=0
    num_games = len(teamGames)
    #Iterate through teamGames to tabulate team data
    for game in teamGames.items():
        game_id, game_data = game
        total_game_time += game_data['team_game']['game_length']
        total_kills += game_data['team_game_combat']['kills']
        total_deaths += game_data['team_game_combat']['deaths']
        total_gold += game_data['team_game_economy']['totalgold']
        total_towers += game_data['team_game_objectives']['towers']
        if game_data['team_game']['result'] == True:
            games_won += 1
        if game_data['team_game_objectives']['firstdragon'] == True:
            first_dragon_games += 1
        if game_data['team_game_objectives']['firstherald'] == True:
            first_herald_games += 1
        if game_data['team_game_combat']['firstblood'] == True:
            first_blood_games += 1
        if game_data['team_game_objectives']['firsttower'] == True:
            first_tower_games += 1
        if game_data['team_game_objectives']['firstbaron'] == True:
            first_baron_games += 1
    #Get Combined Stats, over-under percentages.
    combined_kills = 0
    combined_gold = 0
    combined_towers = 0
    combined_dragons = 0
    combined_barons = 0
    kills_over23 = 0
    kills_over25 = 0
    kills_over27 = 0
    kills_over29 = 0
    towers_over10 = 0
    towers_over11 = 0
    towers_over12 = 0
    dragons_over4 = 0
    dragons_over5 = 0
    barons_over1 = 0
    inhibitors_over1 = 0
    for combined_game in combinedTeamGames:
        #Kill Over Counters
        if combined_game['total_kills'] > 29.5:
            kills_over23 += 1
            kills_over25 += 1
            kills_over27 += 1
            kills_over29 += 1
        elif combined_game['total_kills'] > 27.5:
            kills_over23 += 1
            kills_over25 += 1
            kills_over27 += 1
        elif combined_game['total_kills'] > 25.5:
            kills_over23 += 1
            kills_over25 += 1
        elif combined_game['total_kills'] > 23.5:
            kills_over23 += 1
            
        #Tower Over Counters
        if combined_game['total_towers'] > 12.5:
            towers_over10 += 1
            towers_over11 += 1
            towers_over12 += 1
        elif combined_game['total_towers'] > 11.5:
            towers_over10 += 1
            towers_over11 += 1
        elif combined_game['total_towers'] > 10.5:
            towers_over10 += 1
            
        #Dragons
        if combined_game['total_dragons'] > 5.5:
            dragons_over4 += 1
            dragons_over5  += 1
        elif combined_game['total_dragons'] > 4.5:
            dragons_over4 += 1
            
        #Barons
        if combined_game['total_barons'] > 1.5:
            barons_over1 += 1
        #Inhibs
        if combined_game['total_inhibitors'] > 1.5:
            inhibitors_over1 += 1
            
        #Sum for combined
        combined_kills += combined_game['total_kills']
        combined_gold += combined_game['total_gold']
        combined_towers += combined_game['total_towers']
        combined_dragons += combined_game['total_dragons']
        combined_barons += combined_game['total_barons']
    
    
    return {
        'team_name':teaminfo['team_name'],
        'team_id': game_data['team_game']['team_id'],
        'num_games':num_games,
        'win_rate': games_won/num_games,
        'first_blood_pct': first_blood_games/num_games,
        'first_herald_pct': first_herald_games/num_games,
        'first_tower_pct':first_tower_games/num_games,
        'first_dragon_pct':first_dragon_games/num_games,
        'first_baron_pct':first_baron_games/num_games,
        'avg_length': total_game_time/num_games,
        'avg_kills': total_kills/num_games,
        'avg_deaths': total_deaths/num_games,
        'avg_gold':total_gold/num_games,
        'c_kills': combined_kills/num_games,
        'c_gold':combined_gold/num_games,
        'c_dragons':combined_dragons/num_games,
        'c_towers':combined_towers/num_games,
        'c_barons':combined_barons/num_games,
        'kills_over23':kills_over23/num_games,
        'kills_over25':kills_over25/num_games,
        'kills_over27':kills_over27/num_games,
        'kills_over29':kills_over29/num_games,
        'towers_over10':towers_over10/num_games,
        'towers_over11':towers_over11/num_games,
        'towers_over12':towers_over12/num_games,
        'dragons_over4':dragons_over4/num_games,
        'dragons_over5':dragons_over5/num_games,
        'barons_over1':barons_over1/num_games,
        'inhibitors_over1':inhibitors_over1/num_games,
    }
