"""
Task 1.3: FIFA World Cup Simulation System
----------------------------------------------
A beginner-level OOP implementation of the four core classes:
Player, Team, MatchEvent, and Match. Runs a full 90-minute simulated
match and prints the final score plus the goal timeline.

Note: this covers the core (non-bonus) requirements only, kept simple
on purpose (no AI coach, substitutions, or discipline system).
"""

import random


class Player:
    """A single athlete with attack/defense ratings and stamina."""

    def __init__(self, name, position, base_attack, base_defense):
        self.name = name
        self.position = position  # "FORWARD", "MIDFIELDER", "DEFENDER", "GOALKEEPER"
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.stamina = 100.0  # everyone starts fully rested

    def deplete_stamina(self, rate=0.5):
        """Lowers stamina each minute, but never below the 10.0 floor."""
        self.stamina = max(10.0, self.stamina - rate)

    def get_effective_attack(self):
        """Attack power scaled down as the player gets tired."""
        return self.base_attack * (self.stamina / 100.0)

    def get_effective_defense(self):
        """Defense power scaled down as the player gets tired."""
        return self.base_defense * (self.stamina / 100.0)


class Team:
    """A squad of players with 11 currently on the field (active_lineup)."""

    def __init__(self, country_name, active_lineup):
        self.country_name = country_name
        self.active_lineup = active_lineup  # list of 11 Player objects

    def get_aggregate_attack(self):
        """Average effective attack of all FORWARD + MIDFIELDER players."""
        attackers = [
            p for p in self.active_lineup if p.position in ("FORWARD", "MIDFIELDER")
        ]
        if not attackers:
            return 0.0
        return sum(p.get_effective_attack() for p in attackers) / len(attackers)

    def get_aggregate_defense(self):
        """Average effective defense of all DEFENDER + GOALKEEPER players."""
        defenders = [
            p for p in self.active_lineup if p.position in ("DEFENDER", "GOALKEEPER")
        ]
        if not defenders:
            return 0.0
        return sum(p.get_effective_defense() for p in defenders) / len(defenders)


class MatchEvent:
    """
    An immutable record of something that happened in the match.
    Once created, none of its fields should be changed.
    """

    def __init__(self, event_id, event_type, minute, team, player, outcome_text):
        self.event_id = event_id
        self.event_type = event_type  # "GOAL", "HALF_TIME", "FULL_TIME", etc.
        self.minute = minute
        self.team = team
        self.player = player  # can be None for team-level events
        self.outcome_text = outcome_text

    def to_string(self):
        """Read-only formatted string for displaying this event."""
        player_name = self.player.name if self.player else ""
        return (
            f"[{self.minute}'] {self.event_type} - "
            f"{self.team.country_name} {player_name}: {self.outcome_text}"
        )


class Match:
    """Runs the minute-by-minute simulation between two teams."""

    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.current_minute = 0
        self.timeline = []
        self.phase = "REGULATION"
        self._next_id_number = 1

    def _make_event_id(self):
        event_id = f"E{self._next_id_number}"
        self._next_id_number += 1
        return event_id

    def run_minute_tick(self):
        """Advances the match by one minute: stamina decay + goal checks."""
        self.current_minute += 1

        # Every active player on both teams loses a bit of stamina
        for player in self.home_team.active_lineup + self.away_team.active_lineup:
            player.deplete_stamina(rate=0.5)

        # Each team gets a chance to score this minute
        self.process_goal_attempt(self.home_team, self.away_team)
        self.process_goal_attempt(self.away_team, self.home_team)

    def process_goal_attempt(self, attacking_team, defending_team):
        """
        10% chance per minute that a team even attempts to score.
        If they do, compare a randomized attack rating against a
        randomized (and boosted) defense rating to decide if it's a goal.
        """
        if random.random() >= 0.10:
            return  # no scoring attempt this minute

        attack_rating = attacking_team.get_aggregate_attack() * random.uniform(0.75, 1.25)
        defense_rating = (
            defending_team.get_aggregate_defense() * 1.3 * random.uniform(0.80, 1.20)
        )

        if attack_rating > defense_rating:
            if attacking_team is self.home_team:
                self.home_score += 1
            else:
                self.away_score += 1

            # Pick a scorer from forwards/midfielders if possible
            candidates = [
                p for p in attacking_team.active_lineup
                if p.position in ("FORWARD", "MIDFIELDER")
            ]
            scorer = random.choice(candidates) if candidates else random.choice(
                attacking_team.active_lineup
            )

            event = MatchEvent(
                event_id=self._make_event_id(),
                event_type="GOAL",
                minute=self.current_minute,
                team=attacking_team,
                player=scorer,
                outcome_text=f"{scorer.name} scores!",
            )
            self.timeline.append(event)

    def simulate_full_match(self):
        """Runs all 90 minutes, then marks the match as finished."""
        for _ in range(90):
            self.run_minute_tick()
        self.phase = "FINISHED"

    def print_result(self):
        """Prints the final score, winner, and the goal timeline."""
        print(
            f"Final score: {self.home_team.country_name} {self.home_score} - "
            f"{self.away_score} {self.away_team.country_name}"
        )

        if self.home_score > self.away_score:
            print(f"{self.home_team.country_name} wins!")
        elif self.away_score > self.home_score:
            print(f"{self.away_team.country_name} wins!")
        else:
            print("It's a DRAW!")

        print("\nMatch timeline:")
        if not self.timeline:
            print("(no goals scored)")
        for event in self.timeline:
            print(event.to_string())


def build_sample_team(country_name):
    """Builds a simple 11-player squad: 1 GK, 4 DEF, 4 MID, 2 FWD."""
    positions = (
        ["GOALKEEPER"] + ["DEFENDER"] * 4 + ["MIDFIELDER"] * 4 + ["FORWARD"] * 2
    )
    lineup = []
    for i, position in enumerate(positions):
        name = f"{country_name}_Player{i + 1}"
        player = Player(
            name=name,
            position=position,
            base_attack=random.randint(60, 90),
            base_defense=random.randint(60, 90),
        )
        lineup.append(player)
    return Team(country_name, lineup)


if __name__ == "__main__":
    random.seed(42)  # fixed seed so results are reproducible for testing

    team_a = build_sample_team("ARG")
    team_b = build_sample_team("FRA")

    match = Match(team_a, team_b)
    match.simulate_full_match()
    match.print_result()
