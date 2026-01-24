from pymongo import AsyncMongoClient
import json
import os

# Prendo le variabili d'ambiente
mongo_host = os.getenv("MONGO_HOST", "mongo")
mongo_port = int(os.getenv("MONGO_PORT", 27017))
mongo_db_name = os.getenv("MONGO_DB", "livescore_db")

# DB Mongo con cui posso interagire
client = AsyncMongoClient(mongo_host, mongo_port)

# Apro DB e collezioni necessarie
db = client[mongo_db_name]
running_matches = db["running"]
ended_matches = db["ended"]
scheduled_matches = db["scheduled"]

def open_teams(p = "backend/teams/football.json"):
    global team_data

    # File di dati sulle squadre
    with open(p) as f:
        return json.loads(f.read())


if __name__ == '__main__':

    PATH = "teams/football.json"
    team_data = open_teams(PATH)
    print(team_data)