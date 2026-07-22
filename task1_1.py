"""
Task 1.1: Group Stage Standings Engine
----------------------------------------
Asks the user for the score of each of the 6 matches in a 4-team group,
then prints the final standings table sorted the way FIFA sorts it:
  1) Points (highest first)
  2) Goal Difference (highest first)
  3) Goals Scored (highest first)
"""


def process_match(standings, team1, team2, team1_goals, team2_goals):
    """Updates both teams' stats after one match is played."""

    # Both teams played one more match
    standings[team1]["P"] += 1
    standings[team2]["P"] += 1

    # Add goals scored (GF) and goals conceded (GA) for each team
    standings[team1]["GF"] += team1_goals
    standings[team1]["GA"] += team2_goals
    standings[team2]["GF"] += team2_goals
    standings[team2]["GA"] += team1_goals

    # Decide win / draw / loss
    if team1_goals > team2_goals:
        standings[team1]["W"] += 1
        standings[team1]["Pts"] += 3
        standings[team2]["L"] += 1
    elif team2_goals > team1_goals:
        standings[team2]["W"] += 1
        standings[team2]["Pts"] += 3
        standings[team1]["L"] += 1
    else:
        standings[team1]["D"] += 1
        standings[team2]["D"] += 1
        standings[team1]["Pts"] += 1
        standings[team2]["Pts"] += 1

    # Goal Difference is always recalculated from scratch: GF - GA
    standings[team1]["GD"] = standings[team1]["GF"] - standings[team1]["GA"]
    standings[team2]["GD"] = standings[team2]["GF"] - standings[team2]["GA"]


def get_score_input(team1, team2):
    """Keeps asking the user for a score until they type a valid 'X-Y' format."""
    while True:
        raw = input(f"Enter score for {team1} vs {team2} (format: 2-0): ").strip()
        parts = raw.split("-")

        # Must split into exactly 2 pieces, and both must be whole numbers
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return int(parts[0]), int(parts[1])

        print("Invalid format. Please enter the score like this: 2-0")


def format_gd(gd):
    """Formats Goal Difference with a leading sign: +3, -4, or plain 0."""
    if gd > 0:
        return f"+{gd}"
    elif gd < 0:
        return str(gd)  # negative numbers already show their own '-'
    else:
        return "0"


def print_standings(standings):
    """Prints the standings table sorted by Points, then GD, then GF."""

    # sorted() with a negative key sorts from highest to lowest
    sorted_teams = sorted(
        standings.items(),
        key=lambda item: (-item[1]["Pts"], -item[1]["GD"], -item[1]["GF"]),
    )

    header = f"{'Team':<6}{'P':<4}{'W':<4}{'D':<4}{'L':<4}{'GF':<5}{'GA':<5}{'GD':<5}{'Pts':<4}"
    print(header)

    for team_name, stats in sorted_teams:
        row = (
            f"{team_name:<6}{stats['P']:<4}{stats['W']:<4}{stats['D']:<4}"
            f"{stats['L']:<4}{stats['GF']:<5}{stats['GA']:<5}"
            f"{format_gd(stats['GD']):<5}{stats['Pts']:<4}"
        )
        print(row)


def main():
    teams = ["ARG", "MEX", "POL", "KSA"]

    # Build the starting standings dictionary, all stats at zero
    standings = {
        team: {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}
        for team in teams
    }

    # The 6 fixed matchups for a 4-team round robin group
    matchups = [
        ("ARG", "MEX"),
        ("ARG", "POL"),
        ("ARG", "KSA"),
        ("MEX", "POL"),
        ("MEX", "KSA"),
        ("POL", "KSA"),
    ]

    for team1, team2 in matchups:
        goals1, goals2 = get_score_input(team1, team2)
        process_match(standings, team1, team2, goals1, goals2)

    print()
    print_standings(standings)


if __name__ == "__main__":
    main()
