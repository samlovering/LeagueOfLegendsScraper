#This contains the api functions for the LoLEsportsAPI
#Samuel Lovering
#
#leo.pirker@lopis.de sample api code found from.
#https://vickz84259.github.io/lolesports-api-docs/ -- API Documentation

import json
import requests

class LolEsportsApi:
    API_KEY = {'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'}
    API_URL = 'https://esports-api.lolesports.com/persisted/gw'
    LIVESTATS_API = 'https://feed.lolesports.com/livestats/v1'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.API_KEY)

    def getLeagues(self, hl='en-US'):
        response = self.session.get(
            self.API_URL + '/getLeagues',
            params={'hl': hl}
        )

        return json.loads(response.text)['data']

    def getSchedule(self, hl='en-US', league_id=None):
        response = self.session.get(
            self.API_URL + '/getSchedule',
            params = {
                'hl': hl,
                'leagueId': league_id
            }
        )
        return json.loads(response.text)['data']

    def getTournamentsForLeague(self, hl='en-US', league_id=None):
        response = self.session.get(
            self.API_URL + '/getTournamentsForLeague',
            params={
                'hl': hl,
                'leagueId': league_id
            }
        )
        return json.loads(response.text)['data']

    def getStandings(self, hl='en-US', tournament_id=None):
        response = self.session.get(
            self.API_URL + '/getStandings',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )

        return json.loads(response.text)['data']

    def getCompletedEvents(self, hl='en-US', tournament_id=None):
        response = self.session.get(
            self.API_URL + '/getCompletedEvents',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )

        return json.loads(response.text)['data']

    def getGames(self, hl='en-US', match_id=None):
        response = self.session.get(
            self.API_URL + '/getGames',
            params={
                'hl': hl,
                'id': match_id
            }
        )
        return json.loads(response.text)['data']

    def getEventDetails(self,hl='en-US',match_id=None):
        response = self.session.get(
            self.API_URL + '/getEventDetails',
            params={
                'hl': hl,
                'id': match_id
            }
        )
        return json.loads(response.text)['data']

    def getTeams(self, hl='en-US', team_slug=None):
        response = self.session.get(
            self.API_URL + '/getTeams',
            params={
                'hl': hl,
                'id': team_slug
            }
        )

        return json.loads(response.text)['data']

    def getLive(self, hl='en-US'):
        response = self.session.get(
            self.API_URL + '/getLive',
            params={'hl': hl}
        )

        return json.loads(response.text)['data']

    def getDetails(self,game_id,starting_time=None, playerIDs=None):
        response= self.session.get(
            self.LIVESTATS_API + f'/details/{game_id}',
            params={
                'startingTime': starting_time,
                'participantIds': playerIDs
            }
        )
        return json.loads(response.text)

    def getWindow(self,game_id,starting_time=None):
        response = self.session.get(
            self.LIVESTATS_API + f'/window/{game_id}',
            params={
                'startingTime': starting_time
            }
        )
        return json.loads(response.text)


lolAPI = LolEsportsApi()