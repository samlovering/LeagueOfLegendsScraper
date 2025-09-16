'''
League of Legends - Kill Prediction

Samuel Lovering - 3/12/24

'''

from typing import List

import numpy as np
from database import team_db
from scipy.stats import poisson, norm


def getPredictionData(team1_id: str, team2_id: str) -> List[dict]:
    #Get kills of team 1 and team 2
    team1_data = team_db.getCombinedTeamGames(team1_id)
    team2_data = team_db.getCombinedTeamGames(team2_id)
    team1_total_kills = [float(game['total_kills']) for game in team1_data]
    team2_total_kills = [float(game['total_kills']) for game in team2_data]
    total_kills_per_game = np.array(team1_total_kills + team2_total_kills)
    print(total_kills_per_game)
    team1_avg = np.mean(team1_total_kills)
    print(team1_avg)
    team2_avg = np.mean(team2_total_kills)
    print(team2_avg)
    mean_kills = np.mean(total_kills_per_game)
    std_kills = np.std(total_kills_per_game,ddof=1)
    
    poisson_distribution = poisson(mu=mean_kills)
    
    simulated_poisson_kills = poisson_distribution.rvs(size=1000)
    poisson_percentiles = np.percentile(simulated_poisson_kills, [25, 50, 75])
    
    simulated_normal_kills = norm.rvs(loc=mean_kills, scale=std_kills, size=1000)
    normal_percentiles = np.percentile(simulated_normal_kills, [25, 50, 75])
    normal_1_std_range = (mean_kills - std_kills, mean_kills + std_kills)
    
    print(f"Predicted Total Kills (Poisson): {np.mean(simulated_poisson_kills):.2f}")
    print(f"Prediction Range (Poisson 25th-75th percentile): {poisson_percentiles[0]:.0f} - {poisson_percentiles[2]:.0f}")

    print(f"Predicted Total Kills (Normal): {np.mean(simulated_normal_kills):.2f}")
    print(f"Prediction Range (Normal 25th-75th percentile): {normal_percentiles[0]:.0f} - {normal_percentiles[2]:.0f}")
    print(f"1 Standard Deviation Range (Normal): {normal_1_std_range[0]:.2f} - {normal_1_std_range[1]:.2f}")

def createPoissonKillEstimates(team1_id: str, team2_id: str, over_under: List[float]) -> List[dict]:
    #Get Game data of both teams
    team1_data = team_db.getCombinedTeamGames(team1_id)
    team2_data = team_db.getCombinedTeamGames(team2_id)
    #Parse kills from team data
    team1_total_kills = [float(game['total_kills']) for game in team1_data]
    team2_total_kills = [float(game['total_kills']) for game in team2_data]
    total_kills_per_game = np.array(team1_total_kills + team2_total_kills)
    #Compute Mean of kills
    mean_kills = np.mean(total_kills_per_game)
    #Create Poisson Distribution, evaluator with over/under threshold as 
    print(f"Predicted Total Kills (Mean): {mean_kills:.2f}")
    poisson_distribution = poisson(mu=mean_kills)
    for ou in over_under:
        poisson_prob = 1 - poisson_distribution.cdf(ou)
        print(f"Poisson Model → P(Over {ou} Kills): {poisson_prob:.2%}")
        
def createNormalKillEstimates(team1_id: str, team2_id: str, over_under: List[float]) -> List[dict]:
    #Get Game data of both teams
    team1_data = team_db.getCombinedTeamGames(team1_id)
    team2_data = team_db.getCombinedTeamGames(team2_id)
    #Parse kills from team data
    team1_total_kills = [float(game['total_kills']) for game in team1_data]
    team2_total_kills = [float(game['total_kills']) for game in team2_data]
    total_kills_per_game = np.array(team1_total_kills + team2_total_kills)
    #Compute Mean of kills
    mean_kills = np.mean(total_kills_per_game)
    std_kills = np.std(total_kills_per_game,ddof=1)
    
    for ou in over_under:
        normal_prob = 1 - norm.cdf(ou, loc=mean_kills, scale=std_kills)
        print(f"Normal Model → P(Over {ou} Kills): {normal_prob:.2%}")
     
    