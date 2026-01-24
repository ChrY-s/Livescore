import asyncio
from backend.match_publishers.football.football_pub import FootballMatch

from backend.match_publishers.football.init import reset_disp

from backend.database import open_teams

# Numero match da avviare
stadiums = 5

# Lista match
match_list = []

# Dati sui team
team_data = open_teams()

# Funzione che avvia i generatori di partite
# s = numero partite inizializzate contemporaneamente
async def run_matches(s):
    reset_disp()

    # Avvio le partite
    for _ in range(s):
        m = asyncio.create_task(FootballMatch().run())
        match_list.append(m)



async def main():
    while True:
        await run_matches(stadiums)
        await asyncio.gather(*match_list)


if __name__ == '__main__':
    asyncio.run(main())
