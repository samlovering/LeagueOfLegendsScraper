from typing import List
import database.models as api
from database.db_utils import getSession
import re
import sqlalchemy

'''
Champion Utils
'''

def createChampionDatabase(championList: List[dict]) -> dict:
    with getSession() as session:
        try:
            for champion in championList:
                session.add(api.Champion(**champion))
            session.commit()
            return {"Success":"Champion Database successfully created"}
        except Exception as e:
            session.rollback()
            print(e)
            return {"Error":str(e)}
        
def getChampionByName(championName: str) -> dict:
    with getSession() as session:
        #Verify we have a string passed in.
        if not isinstance(championName, str):
            return {'champion_id':-1}
        
        #Convert edgecase names.
        if championName == 'Wukong':
            championName = 'MonkeyKing'
        elif championName == 'Renata Glasc':
            championName = 'Renata'
        elif championName == 'Nunu & Willump':
            championName = 'Nunu'
            
        championName = re.sub(r'[^\w\s]', '', championName).replace(" ", "")
        champ_query = session.query(api.Champion).filter_by(champion_name = championName).first()
        if champ_query:
            return {
                'champion_id': champ_query.champion_id,
                'champion_name': champ_query.champion_name,
                'champion_image': champ_query.champion_image
            }
        else:
            return {'Error': "Champion {} not found".format(championName)}