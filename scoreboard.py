import csv
import os

file = "scoreboard.csv"

# Create the scoreboard file if it doesn't exist
if not os.path.exists(file):
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Player", "Score", "Games Played", "Wins", "Losses"])

def add_score(player, score, won=True):
    """Add or update a player's score and statistics."""
    updated = False
    rows = []

    with open(file, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row and row[0] == player:
                row[1] = str(int(row[1]) + int(score))        # update score
                row[2] = str(int(row[2]) + 1)                 # games played
                row[3] = str(int(row[3]) + (1 if won else 0)) # wins
                row[4] = str(int(row[4]) + (0 if won else 1)) # losses
                updated = True
            rows.append(row)

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
        if not updated:
            wins = 1 if won else 0
            losses = 0 if won else 1
            writer.writerow([player, score, 1, wins, losses])

def disp_scores():
    """Display the scoreboard with ranks and statistics."""
    sort_scores()
    with open(file, "r") as f:
        reader = csv.reader(f)
        next(reader) #skip header

        # Proper table with aligned columns
        print("+------+----------+-------+--------------+------+--------+")
        print("| Rank |  Player  | Score | Games Played | Wins | Losses |")
        print("+------+----------+-------+--------------+------+--------+")
        
        rank = 1
        for row in reader:
            if row:
                n, s, games, wins, losses = row
                print("| %4d | %8s | %5s | %12s | %4s | %6s |" %
                      (rank, n, s, games, wins, losses))
                rank += 1
        print("+------+----------+-------+--------------+------+--------+")

def sort(l, k):
    """Custom bubble sort by column k."""
    for i in range(len(l)):
        j = 0
        while j < len(l) - 1:
            if int(l[j][k]) < int(l[j+1][k]):  # descending by score
                l[j], l[j+1] = l[j+1], l[j]
            j += 1
    return l

def sort_scores():
    """Sort all scores descending by score (column 1)."""
    with open(file, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    rows = sort(rows, 1)

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def clear_scoreboard():
    """Clear all scores after user confirmation."""
    confirm = input("Are you sure you want to clear the scoreboard? (y/n): ").lower()
    if confirm == "y":
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Player", "Score", "Games Played", "Wins", "Losses"])
        print("Scoreboard cleared!")

def check_existing_user():
    """Return list of existing users."""
    with open(file, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        return [row[0] for row in reader if row]
