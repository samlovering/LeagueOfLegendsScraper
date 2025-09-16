'''
Samuel Lovering
2/24/25

This file either handles connections from api to database, and parses database information when needed.

TODO:
1. Look into adding patch/split/year to seraches

'''

from typing import List, Optional, Union
from database import draft_db

'''
Side selection Win Rate
This Function will query for a teams, region or global side win rate.
'''

def getSideWinRate(
    league: Optional[Union[str,List[str]]]=None, 
    teamId: Optional[Union[str,List[str]]]=None,
    patch: Optional[Union[str,List[str]]]=None
    ) -> dict:
    return draft_db.getSideWinRate(league=league,teamId=teamId,patch=patch)

'''
General Pick/Ban Information

- Get a Teams/Regions top pick bans

'''

def getTopPicks(league: Optional[str]=None, teamId: Optional[str]=None, side: Optional[str]=None) -> List[dict]:
    return draft_db.getPicks(league=league, teamId=teamId,side=side)

def getTopBans(league: Optional[str]=None, teamId: Optional[str]=None, side: Optional[str]=None) -> List[dict]:
    return draft_db.getBans(league=league, teamId=teamId, side=side)

'''
Champion Presence + Priority
'''
def getTopPresence(
    league: Optional[Union[str,List[str]]]=None, 
    teamId: Optional[Union[str,List[str]]]=None, 
    patch: Optional[Union[str,List[str]]]=None, 
    numChamps: int = 10
    ) -> List[dict]:
    return draft_db.getPresence(league=league,teamId=teamId,patch=patch)[:numChamps]


def getTopPrioScore(
    league: Optional[Union[str,List[str]]]=None, 
    teamId: Optional[Union[str,List[str]]]=None, 
    patch: Optional[Union[str,List[str]]]=None, 
    numChamps: int = 10) -> List[dict]:
    return draft_db.getPrioScore(league=league,teamId=teamId,patch=patch)[:numChamps]

'''
Team Synergies

'''
def getSynergies(league: Optional[str]=None,teamId: Optional[str]=None,patch: Optional[str]=None, minGames: Optional[int]=0) -> List[dict]:
    return draft_db.getSynergies(league=league,teamId=teamId,patch=patch,minGames=minGames)


'''
Team Meta Page

-> Win rate per side
-> Bans By Team
-> Bans Against Team
-> Draft Stats
    -> Champ P+B%
    -> Prio Score? 
    -> Common Duos (i.e. mid/jug, jug/sup, adc/sup, top/jg)

'''

def create_team_meta_page(teamId: str) -> dict:
    sideData = getSideWinRate(teamId=teamId)
    print('\nSide Win Rate:')
    for side in sideData:
        print(side)
    blueGames = sideData[0]['total_games']
    redGames = sideData[1]['total_games']
    totalGames = redGames+blueGames
    
    #Bans For
    print('\nRed Side Bans ({} Games)'.format(redGames))
    redBans = (getTopBans(teamId=teamId, side='Red'))
    for ban in redBans[:10]:
        print(ban)
    print('\nBlue Side Bans ({} Games)'.format(blueGames))
    blueBans = (getTopBans(teamId=teamId, side='Blue'))
    for ban in blueBans[:10]:
        print(ban)
    
    #Bans Against
    print('\nAll Bans Against ({} Games)'.format(totalGames))
    allBans = (draft_db.getOpponentBans(teamId=teamId))
    for ban in allBans[:10]:
        print(ban)
    print('\nRed Side Bans Against ({} Games)'.format(redGames))
    redBans = (draft_db.getOpponentBans(teamId=teamId, side='Red'))
    for ban in redBans[:10]:
        print(ban)
    print('\nBlue Side Bans Against ({} Games)'.format(blueGames))
    blueBans = (draft_db.getOpponentBans(teamId=teamId, side='Blue'))
    for ban in blueBans[:10]:
        print(ban)
        
    #Draft Stats
    print('\nPresence %')
    pb_percent = getTopPresence(teamId=teamId)
    for pb in pb_percent[:25]:
        print(f"Champion: {pb['champion_name']:<20} Presence: {(int(pb['count'])/totalGames)*100:>6.2f}%")
        
    print('\nPrio Score ({} Games)'.format(totalGames))
    ps_list = getTopPrioScore(teamId=teamId)
    for ps in ps_list:
       print(f"Champion: {ps['champion_name']:<20} Prio Score: {(ps['score']/(totalGames*100))*100:>6.2f}")
       
    print('\nCommon Synergies')
    synergies = getSynergies(teamId=teamId, minGames=2)
    for syn in synergies:
        print(syn)
        
    print('\nTop Picks')
    topPicks = getTopPicks(teamId=teamId)
    for pick in topPicks[:20]:
        print(pick)

    

'''
Global Meta Page
-> WR per side
-> Highest Presence Champs
-> Draft Stats
    -> Common Duos + WR

'''

def create_global_meta_page(league: Optional[Union[str,List[str]]]=None, patch: Optional[Union[str,List[str]]]=None):
    sideData = getSideWinRate(league=league,patch=patch)
    totalGames = sideData[0]['total_games']
    print('\nSide Win Rate:')
    for side in sideData:
        print(side)
    
    #Draft Stats
    print('\nPresence %')
    pb_percent = getTopPresence(league=league,patch=patch)
    for pb in pb_percent[:25]:
        print(f"Champion: {pb['champion_name']:<20} Presence: {(int(pb['count'])/totalGames)*100:>6.2f}%")
        
    print('\nPrio Score ({} Games)'.format(totalGames))
    ps_list = getTopPrioScore(league=league,patch=patch)
    for ps in ps_list[:25]:
       print(f"Champion: {ps['champion_name']:<20} Prio Score: {(ps['score']/(totalGames*100))*100:>6.2f}")
       
    # print('\nCommon Synergies')
    # synergies = getSynergies(minGames=20)
    # for syn in synergies[:25]:
    #     print(syn)
        
    # print('\nTop Picks')
    # topPicks = getTopPicks()
    # for pick in topPicks[:25]:
    #     print(pick)
        
'''
This creates a TOP region only [LTA, LCK, LPL, LEC, LCP] meta view.

'''
