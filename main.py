"""
Hangman Game with Scoreboard System

Note: This program uses ANSI escape characters to move the cursor around
the terminal for clearing lines, overwriting text, and displaying hangman stages.

Does not work with python IDLE python! Use command prompt to execute the file

/033[A - moves cursor up
/033[B - moves cursor down
/033[C - moves cursor right
/033[D - moves cursor left
/033[E - moves cursor to beginning of next line
/033[F - moves cursor to beginning of previous line
/033[2J - clear screen
"""

import os
from random import randint
import scoreboard as sc

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls')

# Load hangman ASCII art images
hangman_images = []
with open("hangman.txt") as f:
    stage = ""
    for line in f:
        if "#" in line:
            hangman_images.append(stage)
            stage = ""
        else:
            stage += line

def display_hangman(stage_num):
    """Displays hangman stage, clearing previous lines."""
    print("\033[F" * 9, end='')  # move cursor up 9 lines
    print(hangman_images[stage_num], end='')

# Difficulty settings
difficulty_levels = {1: 2, 2: 3, 3: 4}
difficulty_points = {1: 100, 2: 300, 3: 500}
difficulty = 1  # default

# Display game title
clear_screen()
with open("title.txt") as f:
    for line in f:
        print(line, end='')

# Ask for username
existing_users = sc.check_existing_user()
while True:
    name = input("Enter Username (less than 10 letters): ").strip()
    if len(name) > 10 or not name:
        print("Username must be 1-10 characters long.")
        continue
    if name in existing_users:
        use_old = input("This user already exists. Do you want to use this name? (y/n): ").lower()
        if use_old == "y":
            break
        else:
            print("Choose a different username.")
    else:
        break

# Main game loop
while True:
    state = 0
    clear_screen()

    # Main menu
    while True:
        clear_screen()
        print("\n--- Main Menu ---")
        print("1. Play")
        print("2. Change Difficulty")
        print("3. Scoreboard")
        print("4. Clear Scoreboard")
        print("5. Rules")
        try:
            choice = int(input("Enter your choice: "))
            if choice not in [1,2,3,4,5]:
                print("Invalid choice. Choose 1-5.")
                input("Press Enter to continue...")
                continue
        except ValueError:
            print("Invalid input. Enter a number.")
            input("Press Enter to continue...")
            continue

        if choice == 1:
            break
        elif choice == 2:
            while True:
                try:
                    difficulty = int(input(
                        "Choose Difficulty (Points)\n"
                        "1. Easy          100\n"
                        "2. Intermediate  300\n"
                        "3. Hard          500\n"
                        "Enter choice: "
                    ))
                    if difficulty not in [1,2,3]:
                        print("Invalid difficulty. Choose 1-3.")
                        continue
                    break
                except ValueError:
                    print("Enter a number.")
            input("Press Enter to continue...")
        elif choice == 3:
            sc.disp_scores()
            input("Press Enter to return to menu...")
        elif choice == 4:
            sc.clear_scoreboard()
            input("Press Enter to return to menu...")
        elif choice == 5:
            print("Rules:\n"
                "1. First, pick a difficulty – your points depend on it.\n"
                "2. You’ve got 6 chances to mess up before the game’s over.\n"
                "3. Guess the word correctly and you’ll score points based on the difficulty.\n"
                "4. Lose the round and you’ll drop 50 points.\n"
                "5. Play as many rounds as you like until you quit.\n\n"
                "Good luck, and have fun!\n"
            )
            input("Press Enter to return to menu...")

    # Start game
    clear_screen()
    print(hangman_images[state], end='')

    # Pick a random word
    with open("wordbank.txt") as wb:
        words = wb.readlines()
        word = words[randint(0, len(words)-1)].strip().lower()

    # Decide which letters to hide
    hidden_indices = [i for i in range(len(word))]
    for i in range(len(word) // difficulty_levels[difficulty]):
        hidden_indices.pop(randint(0, len(hidden_indices)-1))

    # Guessing loop
    while True:
        # Display word and hangman
        clear_screen()
        display_hangman(state)
        for i in range(len(word)):
            if i in hidden_indices:
                print("_", end="")
            else:
                print(word[i], end="")
        print("\n")

        # Get user guess
        guess = input("Guess a letter: ").strip()
        if not guess or len(guess) != 1:
            print("Enter a single letter.")
            input("Press Enter to continue...")
            continue

        wrong_guess = True
        for i in range(len(word)):
            if word[i] == guess and i in hidden_indices:
                hidden_indices.remove(i)
                wrong_guess = False

        # Win condition
        if not hidden_indices:
            score = difficulty_points[difficulty]
            print("You Won! Score = %d" % score)
            sc.add_score(name, score, won=True)
            input("Press Enter to continue...")
            break

        # Wrong guess handling
        if wrong_guess:
            state += 1

        # Loss condition
        if state == len(hangman_images) - 1:
            clear_screen()
            print(hangman_images[state])
            print("You Lost! The word was: %s" % word)
            sc.add_score(name, -50, won=False)  # negative score for loss
            input("Press Enter to continue...")
            break

    # Continue?
    cont = input("Do you want to continue? (y/n): ").lower()
    if cont == "n":
        print("Thanks for Playing!")
        break
