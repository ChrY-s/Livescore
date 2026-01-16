from Livescore.backend.database import running_matches, scheduled_matches


# -------- INTERAZIONI COL DB --------
# Funzione che inserisce il match dentro il DB
async def create_match(self):

    # Inserisco il match tra i programmati
    await scheduled_matches.insert_one({
        "id": self.id,
        "sport": "calcio",
        "teams": [self.team_1["team_name"], self.team_2["team_name"]],
        "time": self.match_time,
        "scores": self.match_scores,
        "events": self.match_events,
        "schedule": self.match_schedule
    })

    print({
        "id": self.id,
        "sport": "calcio",
        "teams": [self.team_1["team_name"], self.team_2["team_name"]],
        "time": self.match_time,
        "scores": self.match_scores,
        "events": self.match_events,
        "schedule": self.match_schedule
    })


# Aggiornamento della partita in corso nel DB
async def update_match(self):
    await running_matches.update_one(
        {"id": self.id},
        {"$set": {
                        "time": self.match_time,
                        "scores": self.match_scores,
                        "events": self.match_events
                        }
                }
    )
