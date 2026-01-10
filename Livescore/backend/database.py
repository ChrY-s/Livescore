from pymongo import AsyncMongoClient
import json


team_data = {}


# DB Mongo con cui posso interagire
client = AsyncMongoClient("localhost", 27017)

# Collezioni
db = client["livescore_db"]
running_matches = db["running"]
ended_matches = db["ended"]
scheduled_matches = db["scheduled"]

def open_teams(p = "../../teams/football.json"):
    global team_data

    # File di dati sulle squadre                                      ------- DA METTERE NEL DB ------
    with open(p) as f:
        team_data = json.loads(f.read())


open_teams()

if __name__ == '__main__':

    PATH = "teams/football.json"
    open_teams(PATH)