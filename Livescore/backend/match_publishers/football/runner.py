import asyncio
from Livescore.backend.match_publishers.football.football_pub import FootballMatch

from Livescore.backend.match_publishers.football.init import change_availability

from Livescore.backend.database import team_data

# Numero match da avviare
stadiums = 3

# Lista match
match_list = []

# Funzione che avvia i generatori di partite
# s = numero partite inizializzate contemporaneamente
async def run_matches(s):
    for t in team_data:
        # Rendo tutti i team disponibili per una partita
        change_availability(t["team_name"], "y")

    # Avvio le partite
    for _ in range(s):
        m = asyncio.create_task(FootballMatch().run())

        match_list.append(m)


async def main():
    await run_matches(stadiums)
    await asyncio.gather(*match_list)


if __name__ == '__main__':
    asyncio.run(main())
