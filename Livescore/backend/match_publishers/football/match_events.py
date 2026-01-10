import random

# -------- EVENTI --------
# Durante la partita: goal, fallo
# Goal
def goal(self):
    # elemento rnd associato ai goal
    gl_rnd = random.Random()
    # elemento rnd associato a chi ha fatto gol
    pl_rnd = random.Random()

    # scelgo a che squadra va il goal
    if gl_rnd.random() < .5:
        team = self.team_1
        self.match_scores[0] += 1
    else:
        team = self.team_2
        self.match_scores[1] += 1

    # scelgo chi ha fatto gol
    player = None
    while not player:
        possible_player = pl_rnd.choice(team["team_components"])

        # i portieri non possono fare goal
        if possible_player["role"] == "goalkeeper":
            continue

        player = possible_player

    self.match_events.append({"type": "goal",
                              "time": self.match_time,
                              "details": f'{team["team_name"]} ha fatto goal grazie a {player["surname"]} ({player["number"]}) '
                                         f'Punteggio parziale: {self.match_scores}'})


# Fallo
def foul(self):
    # elemento rnd associato ai falli
    fl_rnd = random.Random()
    # elemento rnd associato a chi ha fatto gol
    pl_rnd = random.Random()

    # scelgo
    if fl_rnd.random() < .5:
        bad_team = self.team_1
        sad_team = self.team_2
    else:
        bad_team = self.team_2
        sad_team = self.team_1

    # scelgo chi ha fatto fallo e su chi
    bad = pl_rnd.choice(bad_team["team_components"])
    sad = pl_rnd.choice(sad_team["team_components"])

    self.match_events.append({"type": "foul",
                              "time": self.match_time,
                              "details": f'{bad_team["team_name"]} ha fatto fallo, '
                                         f'{bad["surname"]} su {sad["surname"]} '})