import random
import datetime as timeInfo
import json

from Livescore.backend.database import team_data

# Variabili di controllo ritardi sulla pianificazione delle partite
# 0 = tempo corrente
# n = delay massimo
days_delay = 0
hour_delay = 0
minute_delay = 0
second_delay = 0


# -------- INIZIALIZZAZIONI --------
# Funzione che restituisce un tempo casuale di inizio partita
def schedule_match():
    # Fattori random per un attesa casuale nel prossimo match
    d_rnd = random.Random()
    h_rnd = random.Random()
    m_rnd = random.Random()
    s_rnd = random.Random()

    # Tempo corrente
    now = timeInfo.datetime.now()

    # Restituisco il timestamp di quando il match dovrà iniziare
    return now + timeInfo.timedelta(days=d_rnd.randint(0, days_delay),
                                    hours=h_rnd.randint(0, hour_delay),
                                    minutes=m_rnd.randint(0, minute_delay),
                                    seconds=s_rnd.randint(0, second_delay))


# Funzione che restituisce due squadre casuali, prendendole da quelle non impegnate in partita
def choose_teams():
    team_1 = None
    team_2 = None

    # elemento RND per scegliere le squadre
    rnd = random.Random()

    # Continuo finchè non scelgo entrambi i team
    while not team_1:
        possible_team = rnd.choice(team_data)

        # Se il team è disponibile per una partita lo scelgo
        if possible_team["available"] == "y":
            # Il team non è più disponibile
            change_availability(possible_team["team_name"], "n")
            team_1 = possible_team

    while not team_2:
        possible_team = rnd.choice(team_data)

        # Se il team è disponibile per una partita lo scelgo
        if possible_team["available"] == "y":
            # Il team non è più disponibile
            change_availability(possible_team["team_name"], "n")
            team_2 = possible_team

    return team_1, team_2


# Funzione che cambia la disponibilità di una squadra
def change_availability(team_name, change_to):
    # File di dati sulle squadre
    with open("../../teams/football.json") as f:
        team_data = json.loads(f.read())

        # Cerco la squadra desiderata
        for t in team_data:
            if t["team_name"] == team_name:

                # Faccio una copia della squadra e rimuovo quella vecchia
                copy = t
                team_data.remove(t)

                # Cambio la disponibilità
                if change_to == "n":
                    copy["available"] = "n"
                elif change_to == "y":
                    copy["available"] = "y"

                # Appendo la copia modificata
                team_data.append(copy)

                break

    # Modifico il file json
    with open("../../teams/football.json", "w") as f:
        f.write(json.dumps(team_data))
