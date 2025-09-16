"""
team_stats.py

This handles calcations and queries for team based statistics.

"""

from database import draft_db, player_db, team_db


def getTeamOverview(teamId: str) -> dict:
    """Return an overview of a team with basic info and stats"""
    
    #Get basic team info
    team_info = team_db.getTeamById(teamId)
    
    #Get team Draft stats
    team_picks = draft_db.getPicks(teamId=teamId)
    team_bans = draft_db.getBans(teamId=teamId)
    
    opponent_picks = draft_db.getOpponentPicks(teamId)
    opponent_bans = draft_db.getOpponentBans(teamId)
    
    #Get team stats
    team_basic_stats = team_db.getBasicTeamStats(teamId)
    team_economy = team_db.getTeamEconomyStats(teamId)
    team_combat = team_db.getTeamCombatStats(teamId)
    team_objectives = team_db.getTeamObjectiveStats(teamId)
    team_vision = team_db.getTeamVisionStats(teamId)
    
    #Get team players and then their basic stats.
    team_players = player_db.getPlayersByTeamId(teamId)
    player_stats_list = []
    for player in team_players:
        player_stats = player_db.getBasicPlayerStats(player['player_id'])
        player_stats['player_name'] = player['player_name']
        player_stats['player_id'] = player['player_id']
        player_stats['role'] = player['role']
        player_stats_list.append(player_stats)
    
    team_overview = {
        "team_info": team_info,
        "team_basic_stats": team_basic_stats,
        "team_economy": team_economy,
        "team_combat": team_combat,
        "team_objectives": team_objectives,
        "team_vision": team_vision,
        "draft":{
            "team_picks": team_picks,
            "team_bans": team_bans,
            "opponent_picks": opponent_picks,
            "opponent_bans": opponent_bans,
        },
        "players": player_stats_list,
    }
    return team_overview
    
def getTeamList() -> dict:
    """Return a list of all teams with basic info"""
    teams = team_db.getAllTeams()
    team_stats = team_db.getBasicTeamStats()
    team_list = []
    for team in teams:
        team_id = team['team_id']
        stats = next((stat for stat in team_stats if stat['team_id'] == team_id), None)
        if stats:
            team.update(stats)
        team_list.append(team)
    return team_list
