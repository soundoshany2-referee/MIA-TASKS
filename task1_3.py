import random


class Player:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.stamina = 100

    def reduce_stamina(self):
        if self.stamina > 10:
            self.stamina -= 0.5

    def attack_power(self):
        return self.attack * self.stamina / 100

    def defense_power(self):
        return self.defense * self.stamina / 100


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players

    def attack(self):
        total = 0

        for player in self.players:
            total += player.attack_power()

        return total / len(self.players)

    def defense(self):
        total = 0

        for player in self.players:
            total += player.defense_power()

        return total / len(self.players)


class Match:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.score1 = 0
        self.score2 = 0
        self.events = []

    def play(self):

        for minute in range(1, 91):

            for player in self.team1.players:
                player.reduce_stamina()

            for player in self.team2.players:
                player.reduce_stamina()

            if random.randint(1, 10) == 1:
                if self.team1.attack() > self.team2.defense():
                    self.score1 += 1
                    self.events.append(
                        "Minute " + str(minute) + ": Goal for " + self.team1.name
                    )

            if random.randint(1, 10) == 1:
                if self.team2.attack() > self.team1.defense():
                    self.score2 += 1
                    self.events.append(
                        "Minute " + str(minute) + ": Goal for " + self.team2.name
                    )

    def result(self):
        print(self.team1.name, self.score1, "-", self.score2, self.team2.name)

        if self.score1 > self.score2:
            print("Winner:", self.team1.name)
        elif self.score2 > self.score1:
            print("Winner:", self.team2.name)
        else:
            print("Draw")

        print()

        if len(self.events) == 0:
            print("No goals scored")
        else:
            for event in self.events:
                print(event)


team1 = [
    Player("Player1", 90, 60),
    Player("Player2", 85, 65),
    Player("Player3", 88, 62),
    Player("Player4", 87, 70),
    Player("Player5", 84, 68)
]

team2 = [
    Player("PlayerA", 88, 64),
    Player("PlayerB", 82, 72),
    Player("PlayerC", 86, 66),
    Player("PlayerD", 90, 60),
    Player("PlayerE", 83, 71)
]

argentina = Team("Argentina", team1)
france = Team("France", team2)

match = Match(argentina, france)
match.play()
match.result()