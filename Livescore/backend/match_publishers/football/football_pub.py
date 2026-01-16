import random
import datetime as timeInfo
import asyncio

from Livescore.backend.database import running_matches, scheduled_matches, ended_matches
from Livescore.backend.match_publishers.football.init import schedule_match, choose_teams, change_availability

from Livescore.backend.match_publishers.football.db_interactions import create_match, update_match
from Livescore.backend.match_publishers.football.match_events import goal, foul


# Istanza della partita
class FootballMatch:
    # id partite
    match_id = 1

    def __init__(self):
        # Sport
        self.sport = "calcio"

        # Squadre
        self.team_1, self.team_2 = choose_teams()

        # Id della partita
        self.id = self.__class__.match_id
        self.__class__.match_id += 1

        # Inizio la partita, con entrambe le squadre a 0 punti
        self.match_time = 0
        self.match_scores = [0, 0]
        # Lista eventi durante la partita   {
        #                                       tipo evento,
        #                                       minuto,
        #                                       dettagli
        #                                   }
        self.match_events = []

        # Ora di inizio match programmato
        self.match_schedule = schedule_match()

    async def run(self):
        # Creo il match nel DB
        await create_match(self)

        # Flag che mi dice se la partita è iniziata
        started = False

        # Il match ha inizio
        while True:
            # Controllo il match debba iniziare
            if timeInfo.datetime.now() < self.match_schedule:
                await asyncio.sleep(1)
                continue

            # Se il match inizia lo sposto nei match in corso
            if not started:
                started = True

                start_match = await scheduled_matches.find_one({"id": self.id})

                await scheduled_matches.delete_one(start_match)
                await running_matches.insert_one(start_match)

            # rnd associati agli eventi
            gl_rnd = random.Random()
            fl_rnd = random.Random()

            # Aumento il tempo di gioco di un minuto ogni secondo
            await asyncio.sleep(1)
            self.match_time += 1
            # La partita finisce dopo 90 minuti
            if self.match_time > 90:
                # Sposto la partita nelle partite concluse
                end_match = await running_matches.find_one({"id": self.id})
                await running_matches.delete_one(end_match)
                await ended_matches.insert_one(end_match)

                # I team sono di nuovo disponibili per fare partite
                change_availability(self.team_1["team_name"], "y")
                change_availability(self.team_2["team_name"], "y")
                break

            # c'è una possibilità su 60 che avvenga un goal
            if gl_rnd.random() < .02:
                goal(self)

            # c'è una possibilità su 100 che avvenga un fallo
            if fl_rnd.random() < .01:
                foul(self)

            # aggiorno la partita
            await update_match(self)


# Avvio i publisher delle partite
async def run_matches():
    m = FootballMatch()
    await m.run()

async def main():
    # Alla fine di un match ne inizia un altro
    while True:
        await run_matches()


if __name__ == '__main__':
    asyncio.run(main())
