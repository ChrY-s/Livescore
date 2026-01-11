from pymongo import AsyncMongoClient
import json

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
        return json.loads(f.read())


if __name__ == '__main__':

    PATH = "teams/football.json"
    team_data = open_teams(PATH)
    print(team_data)