def process_match(standings, team1, team2, goals1, goals2):

    standings[team1]["P"] += 1
    standings[team2]["P"] += 1

    standings[team1]["GF"] += goals1
    standings[team1]["GA"] += goals2

    standings[team2]["GF"] += goals2
    standings[team2]["GA"] += goals1

    if goals1 > goals2:
        standings[team1]["W"] += 1
        standings[team2]["L"] += 1
        standings[team1]["Pts"] += 3

    elif goals2 > goals1:
        standings[team2]["W"] += 1
        standings[team1]["L"] += 1
        standings[team2]["Pts"] += 3

    else:
        standings[team1]["D"] += 1
        standings[team2]["D"] += 1
        standings[team1]["Pts"] += 1
        standings[team2]["Pts"] += 1

    standings[team1]["GD"] = standings[team1]["GF"] - standings[team1]["GA"]
    standings[team2]["GD"] = standings[team2]["GF"] - standings[team2]["GA"]


def print_standings(standings):

    teams = sorted(
        standings.items(),
        key=lambda team: (
            team[1]["Pts"],
            team[1]["GD"],
            team[1]["GF"]
        ),
        reverse=True
    )

    print()
    print(f"{'Team':<5} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<4} {'GA':<4} {'GD':<4} {'Pts':<4}")

    for team, stats in teams:

        if stats["GD"] > 0:
            gd = "+" + str(stats["GD"])
        elif stats["GD"] < 0:
            gd = str(stats["GD"])
        else:
            gd = "0"

        print(
            f"{team:<5} "
            f"{stats['P']:<3} "
            f"{stats['W']:<3} "
            f"{stats['D']:<3} "
            f"{stats['L']:<3} "
            f"{stats['GF']:<4} "
            f"{stats['GA']:<4} "
            f"{gd:<4} "
            f"{stats['Pts']:<4}"
        )


def main():

    teams = ["ARG", "MEX", "POL", "KSA"]

    standings = {}

    for team in teams:
        standings[team] = {
            "P": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "Pts": 0
        }

    matches = [
        ("ARG", "MEX"),
        ("ARG", "POL"),
        ("ARG", "KSA"),
        ("MEX", "POL"),
        ("MEX", "KSA"),
        ("POL", "KSA")
    ]

    for team1, team2 in matches:

        while True:

            score = input(f"Enter score for {team1} vs {team2} (format: 2-0): ")

            try:
                goals1, goals2 = score.split("-")
                goals1 = int(goals1)
                goals2 = int(goals2)
                break

            except ValueError:
                print("Invalid input. Please enter the score in the format X-Y.")

        process_match(standings, team1, team2, goals1, goals2)

    print_standings(standings)


if name == "main":
    main()