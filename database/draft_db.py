from itertools import combinations
from typing import List, Optional

from sqlalchemy import Integer, case, func, union_all
from database.db_utils import getSession
import database.models as api

'''
Side Win Rate

While not specifically related to draft, valuable piece of information
'''
def getSideWinRate(league: Optional[str]=None,teamId: Optional[str]=None) -> List[dict]:
    with getSession() as session:
        #Create a base query
        side_query = session.query(api.Team_Game)
        #Apply teamId filter if it exists
        if teamId:
            side_query = side_query.filter(api.Team_Game.team_id == teamId)
        if league:
            side_query = (
                side_query
                .join(api.Team,api.Team_Game.team_id == api.Team.team_id)
                .filter(api.Team.league == league)
            )
        #Query for side win rate
        results = (side_query.with_entities(
            api.Team_Game.side,
            func.count().label('total_games'),
            func.sum(func.cast(api.Team_Game.result, Integer)).label('wins'),
            (func.sum(func.cast(api.Team_Game.result, Integer)) / func.count() * 100).label('win_rate')
            )
            .group_by(api.Team_Game.side)
            .all()
        )
        return[
            {
                "side": side,
                "total_games":total_games,
                "wins":wins,
                "win_rate":win_rate,
            }
            for side, total_games, wins, win_rate in results
        ]
            


'''
Team General Pick Bans.
Get the top num of picks or bans for a team.f

'''
            
def getBans(league: Optional[str] = None, teamId: Optional[str]=None, side: Optional[str]=None) -> List[dict]:
    with getSession() as session:
        #Create a query and filter by league if possible.
        draft_query = session.query(api.Team_Draft).join(api.Team, api.Team_Draft.team_id == api.Team.team_id)
        #If there is a league specifier, add a filter
        if league:
            draft_query = draft_query.filter(api.Team.league == league)
        if teamId:
            draft_query = draft_query.filter(api.Team_Draft.team_id==teamId)
        if side:
            draft_query = draft_query.join(api.Team_Game, api.Team_Draft.team_game_id == api.Team_Game.team_game_id)
            draft_query = draft_query.filter(api.Team_Game.side == side)
         
        ban_columns = union_all(
            draft_query.with_entities(api.Team_Draft.ban1.label('ban'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban2.label('ban'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban3.label('ban'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban4.label('ban'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban5.label('ban'), api.Team.team_id),
            ).alias('all_picks')
        
        results = (
            session.query(
                api.Champion.champion_name,
                func.count(ban_columns.c.ban).label('ban_count')
            )
            .join(api.Champion, ban_columns.c.ban == api.Champion.champion_id)
            .group_by(api.Champion.champion_name)
            .order_by(func.count(ban_columns.c.ban).desc())
            .all()
        )
        
        return [{"champion_name": champion_name, "count": ban_count} for champion_name, ban_count in results]
                        

def getPicks(league: Optional[str] = None, teamId: Optional[str]=None, side: Optional[str]=None) -> List[dict]:
    with getSession() as session:
        #Create a query and filter by league if possible.
        draft_query = session.query(api.Team_Draft).join(api.Team, api.Team_Draft.team_id == api.Team.team_id)
        #If there is a league specifier, add a filter
        if league:
            draft_query = draft_query.filter(api.Team.league == league)
        if teamId:
            draft_query = draft_query.filter(api.Team_Draft.team_id==teamId)
        if side:
            draft_query = draft_query.join(api.Team_Game, api.Team_Draft.team_game_id==api.Team_Game.team_game_id)
            draft_query = draft_query.filter(api.Team_Game.side == side)
            
        #Combines all Picks under "all_picks"
        pick_columns = union_all(
            draft_query.with_entities(api.Team_Draft.pick1.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick2.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick3.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick4.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick5.label('pick_id'), api.Team.team_id),
        ).alias('all_picks')

            
        results = (
            session.query(
                api.Champion.champion_name,
                func.count(pick_columns.c.pick_id).label('pick_count')
            )
            .join(api.Champion,pick_columns.c.pick_id==api.Champion.champion_id)
            .group_by(api.Champion.champion_name)
            .order_by(func.count(pick_columns.c.pick_id).desc())
            .all()
        )
        
        return [{"champion_name": champion_name, "count": pick_count} for champion_name, pick_count in results]


'''
Opposing Team Bans into a Team
'''

def getOpponentBans(teamId: str, side: Optional[str]=None) -> List[dict]:
    with getSession() as session:
        #Get all of a team's games, with an option for specific side
        team_games = (
            session.query(api.Team_Game.game_id, api.Team_Game.side)
            .filter(api.Team_Game.team_id == teamId)
        )
        if side:
            team_games = team_games.filter(api.Team_Game.side == side)
        team_games = team_games.subquery('team_games')  
        
        #Get all opposing teams in those games
        opposing_teams = (
            session.query(api.Team_Game.team_id, api.Team_Game.side, api.Team_Game.team_game_id)
            .join(team_games, api.Team_Game.game_id == team_games.c.game_id)
            .filter(api.Team_Game.team_id != teamId)
            .distinct()
            .subquery('opposing_teams')
        )
        #Create a query that takes the opponents games.
        draft_query = (
            session.query(api.Team_Draft)
            .join(api.Team_Game, api.Team_Draft.team_game_id == api.Team_Game.team_game_id)
            .join(opposing_teams, api.Team_Game.team_game_id == opposing_teams.c.team_game_id)
        )
        if side:
            opposite_side = 'Red' if side == 'Blue' else 'Blue'
            draft_query = draft_query.filter(api.Team_Game.side == opposite_side)

        #Combine all Ban Columns under one.
        ban_columns = union_all(
            draft_query.with_entities(api.Team_Draft.ban1.label('ban')),
            draft_query.with_entities(api.Team_Draft.ban2.label('ban')),
            draft_query.with_entities(api.Team_Draft.ban3.label('ban')),
            draft_query.with_entities(api.Team_Draft.ban4.label('ban')),
            draft_query.with_entities(api.Team_Draft.ban5.label('ban')),
        ).alias('all_bans')
        
        #Query for Results
        results = (
            session.query(
                api.Champion.champion_name,
                func.count(ban_columns.c.ban).label('ban_count')
            )
            .join(api.Champion, ban_columns.c.ban == api.Champion.champion_id)
            .group_by(api.Champion.champion_name)
            .order_by(func.count(ban_columns.c.ban).desc())
            .all()
        )
        
        return [{"champion_name": champion_name, "count": ban_count} for champion_name, ban_count in results]
    
'''
Get Opposing Team Picks
'''
    
def getOpponentPicks(teamId: str, side: Optional[str]=None) -> List[dict]:
    with getSession() as session:
        #Get all of a team's games, with an option for specific side
        team_games = (
            session.query(api.Team_Game.game_id, api.Team_Game.side)
            .filter(api.Team_Game.team_id == teamId)
        )
        if side:
            team_games = team_games.filter(api.Team_Game.side == side)
        team_games = team_games.subquery('team_games')  
        
        #Get all opposing teams in those games
        opposing_teams = (
            session.query(api.Team_Game.team_id, api.Team_Game.side, api.Team_Game.team_game_id)
            .join(team_games, api.Team_Game.game_id == team_games.c.game_id)
            .filter(api.Team_Game.team_id != teamId)
            .distinct()
            .subquery('opposing_teams')
        )
        #Create a query that takes the opponents games.
        draft_query = (
            session.query(api.Team_Draft)
            .join(api.Team_Game, api.Team_Draft.team_game_id == api.Team_Game.team_game_id)
            .join(opposing_teams, api.Team_Game.team_game_id == opposing_teams.c.team_game_id)
        )
        if side:
            opposite_side = 'Red' if side == 'Blue' else 'Blue'
            draft_query = draft_query.filter(api.Team_Game.side == opposite_side)
            
        #Combines all Picks under "all_picks"
        pick_columns = union_all(
            draft_query.with_entities(api.Team_Draft.pick1.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick2.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick3.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick4.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick5.label('pick_id'), api.Team.team_id),
        ).alias('all_picks')

            
        results = (
            session.query(
                api.Champion.champion_name,
                func.count(pick_columns.c.pick_id).label('pick_count')
            )
            .join(api.Champion,pick_columns.c.pick_id==api.Champion.champion_id)
            .group_by(api.Champion.champion_name)
            .order_by(func.count(pick_columns.c.pick_id).desc())
            .all()
        )
        
        return [{"champion_name": champion_name, "count": pick_count} for champion_name, pick_count in results]
    
'''
Draft Scoring
This assesses drafts by two factors, one by general presence percentage (pick + ban percent) or

Prio Score, which uses the following to score prio based on posistion in draft:

1st Ban Phase - 100 pts (These are where must bans go)
2nd Ban Phase - 50 pts (picks 4/5 are weighted significantly lower than earlier picks)
Picks - 100pts/{pick position}

'''

def getPresence(
    league: Optional[str]=None, 
    teamId: Optional[str]=None, 
    patch: Optional[str]=None,
)->List[dict]:
    with getSession() as session:
    #Create a basic query for the Team_Draft Table
        draft_query =( 
            session.query(api.Team_Draft)
            .join(api.Game, api.Game.game_id == api.Team_Draft.game_id)
            .join(api.Team, api.Team.team_id == api.Team_Draft.team_id))
        
        if league:
            draft_query = draft_query.filter(api.Team.league == league)
        if patch:
            draft_query = draft_query.filter(api.Game.patch == patch)
        if teamId:
            draft_query = draft_query.filter(
                (api.Game.team1_id == teamId) | (api.Game.team2_id == teamId)
            )
            
        #Combines all Picks under "all_picks"
        presence_columns = union_all(
            draft_query.with_entities(api.Team_Draft.pick1.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick2.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick3.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick4.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.pick5.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban1.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban2.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban3.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban4.label('pick_id'), api.Team.team_id),
            draft_query.with_entities(api.Team_Draft.ban5.label('pick_id'), api.Team.team_id),
        ).alias('presence')
        
    
        results = (
            session.query(
                api.Champion.champion_name,
                func.count(presence_columns.c.pick_id).label('pick_count')
            )
            .join(api.Champion,presence_columns.c.pick_id==api.Champion.champion_id)
            .group_by(api.Champion.champion_name)
            .order_by(func.count(presence_columns.c.pick_id).desc())
            .all()
        )

        return [{"champion_name": champion_name, "count": pick_count} for champion_name, pick_count in results]
            
def getPrioScore(
    league: Optional[str]=None,
    teamId: Optional[str]=None,
    patch: Optional[str]=None,
) -> List[dict]:
    with getSession() as session:
        #Create a basic query for the Team_Draft Table
        draft_query =( 
            session.query(api.Team_Draft)
            .join(api.Game, api.Game.game_id == api.Team_Draft.game_id)
            .join(api.Team, api.Team.team_id == api.Team_Draft.team_id))
        
        if league:
            draft_query = draft_query.filter(api.Team.league == league)
        if patch:
            draft_query = draft_query.filter(api.Game.patch == patch)
        if teamId:
            draft_query = draft_query.filter(
                (api.Game.team1_id == teamId) | (api.Game.team2_id == teamId)
            )
            
        # Combine all picks and bans into a single column with scores
        prio_scores = union_all(
            draft_query.with_entities(
                api.Team_Draft.pick1.label('champion_id'),
                case((api.Team_Draft.pick1 != -1, 100), else_=0).label('score')
            ),
            draft_query.with_entities(
                api.Team_Draft.pick2.label('champion_id'),
                case((api.Team_Draft.pick2 != -1, 50), else_=0).label('score') 
            ),
            draft_query.with_entities(
                api.Team_Draft.pick3.label('champion_id'),
                case((api.Team_Draft.pick3 != -1, 33), else_=0).label('score') 
            ),
            draft_query.with_entities(
                api.Team_Draft.pick4.label('champion_id'),
                case((api.Team_Draft.pick4 != -1, 25), else_=0).label('score')  
            ),
            draft_query.with_entities(
                api.Team_Draft.pick5.label('champion_id'),
                case((api.Team_Draft.pick5 != -1, 20), else_=0).label('score')  
            ),
            draft_query.with_entities(
                api.Team_Draft.ban1.label('champion_id'),
                case((api.Team_Draft.ban1 != -1, 100), else_=0).label('score') 
            ),
            draft_query.with_entities(
                api.Team_Draft.ban2.label('champion_id'),
                case((api.Team_Draft.ban2 != -1, 100), else_=0).label('score') 
            ),
            draft_query.with_entities(
                api.Team_Draft.ban3.label('champion_id'),
                case((api.Team_Draft.ban3 != -1, 100), else_=0).label('score')  
            ),
            draft_query.with_entities(
                api.Team_Draft.ban4.label('champion_id'),
                case((api.Team_Draft.ban4 != -1, 50), else_=0).label('score')
            ),
            draft_query.with_entities(
                api.Team_Draft.ban5.label('champion_id'),
                case((api.Team_Draft.ban5 != -1, 50), else_=0).label('score')
            ),
        ).alias('prio_score')
        
        # Calculate total scores for each champion
        results = (
            session.query(
                api.Champion.champion_name,
                func.sum(prio_scores.c.score).label('total_score')
            )
            .join(api.Champion, prio_scores.c.champion_id == api.Champion.champion_id)
            .group_by(api.Champion.champion_name)
            .order_by(func.sum(prio_scores.c.score).desc())
            .all()
        )
        return [{"champion_name": champion_name, "score": champ_score} for champion_name, champ_score in results]    
        
'''
Champion Performance

This section details champion stats compared to other champions

'''
def getSynergies(
    league: Optional[str]=None, 
    teamId: Optional[str]=None, 
    patch: Optional[str]=None,
    minGames: Optional[int]=0,
)->List[dict]:
    with getSession() as session:
        #Create a query to search for team picks
        base_query = (
            session.query(api.Team_Draft)
            .join(api.Team, api.Team_Draft.team_id==api.Team.team_id)
            .join(api.Team_Game, api.Team_Draft.team_game_id==api.Team_Game.team_game_id)
            .join(api.Game, api.Team_Draft.game_id == api.Game.game_id)
        )
        #Add filters based on league/teamId/patch version
        if league:
            base_query = base_query.filter(api.Team.league==league)
        if teamId:
            base_query = base_query.filter(api.Team_Draft.team_id==teamId)
        if patch:
            base_query = base_query.filter(api.Game.patch == patch)
            
        #Query for duo synergies
        drafts = (
            base_query.with_entities(
                api.Team_Draft.team_game_id,
                api.Team_Draft.pick1,
                api.Team_Draft.pick2,
                api.Team_Draft.pick3,
                api.Team_Draft.pick4,
                api.Team_Draft.pick5,
                api.Team_Game.result,
            )
            .all()
        )
        champion_names = {
            champion.champion_id: champion.champion_name
            for champion in session.query(api.Champion).all()
        }
        
        duo_data = {}
        #Iterate through the drafts, pick out champ pairs and whether it won or not.
        for draft in drafts:
            picks = [draft.pick1,draft.pick2,draft.pick3,draft.pick4,draft.pick5]
            picks = [pick for pick in picks if pick is not None]
            
            for pair in combinations(picks, 2):
                sorted_pair = tuple(sorted(pair))
                if sorted_pair not in duo_data:
                    duo_data[sorted_pair] = {"count":0,"wins":0}
                duo_data[sorted_pair]["count"]+=1
                if draft.result == 1:
                    duo_data[sorted_pair]["wins"]+=1

        
        results = [
            {
                "champion_1": champion_names[pair[0]],
                "champion_2": champion_names[pair[1]],
                "count": data["count"],
                "wins": data["wins"],
                "win_rate": (data["wins"] / data["count"]) * 100 if data["count"] > 0 else 0,
            }
            for pair, data in duo_data.items() if data['count'] > minGames
        ]
        #If minGames if higher than 5, sort by win_rate, else sort by game count
        if minGames > 5:
            results_sorted = sorted(results, key=lambda x: x["win_rate"], reverse=True)
        else:
            results_sorted = sorted(results, key=lambda x: x["count"], reverse=True)
            
        return results_sorted