import random
import datetime as timeInfo
import json

from Livescore.backend.database import open_teams

# Dati sui team
team_data = open_teams()

# Variabili di controllo ritardi sulla pianificazione delle partite
# 0 = tempo corrente
# n = delay massimo
days_delay = 1
hour_delay = 2
minute_delay = 10
second_delay = 30


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

    #for t in team_data:
    #    print(f'{t["team_name"]}: {t["available"]}')

    return team_1, team_2


# Funzione che cambia la disponibilità di una squadra
def change_availability(team_name, change_to):
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
    with open("backend/teams/football.json", "w") as f:
        f.write(json.dumps(team_data))


# Funzione che riporta tutti i team a disponibile
def reset_disp():
    # Lista nomi team
    teams = []
    for t in team_data:
        teams.append(t['team_name'])

    for t in teams:
        # Rendo tutti i team disponibili per una partita
        change_availability(t, "y")


if __name__ == '__main__':
    reset_disp()
    for _ in range(5):
        print(choose_teams())
