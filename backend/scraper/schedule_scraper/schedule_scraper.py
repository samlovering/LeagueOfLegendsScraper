from datetime import datetime
from typing import List, Optional
from scraper.web_connections.lol_esports import lolAPI
from database import team_db

'''
This returns upcomming matches for a specified league ()

league - List[str] -> list of league names
end_date - end range for upcomming matches

'''

def get_upcomming_matches(leagues: Optional[List[str]]=None, end_date: Optional[datetime]=None) -> List[dict]: 
    upcoming_matches = []
    if leagues:
        for league_id in leagues:
            schedule = (lolAPI.getSchedule(league_id=league_id)) 
            for event in schedule['schedule']['events']:
                if event['state'] != 'completed':
                    if end_date:
                        event_start_time = datetime.fromisoformat(event['startTime']).replace(tzinfo=None)
                        if event_start_time < end_date:
                            upcoming_matches.append(event)
                    else:
                        upcoming_matches.append(event)
    else:
        # If no league is specified, fetch all leagues (you may need to adjust this logic)
        schedule = lolAPI.getSchedule()
        for event in schedule['schedule']['events']:
            if event['state'] != 'completed':
                if end_date:
                    event_start_time = datetime.fromisoformat(event['startTime']).replace(tzinfo=None)
                    if event_start_time < end_date:
                        upcoming_matches.append(event)
                else:
                    upcoming_matches.append(event)

    return upcoming_matches