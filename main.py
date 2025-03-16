from datetime import datetime
import math
import os
import random
import time


# Funkcja do pobierania nicku od użytkownika
def get_player_name():
    print("Podaj swój nick:")
    name = input().strip()
    if not name:
        print("Nick nie może być pusty! Użyjemy domyślnego 'Gracz'.")
        name = "Gracz"
    return name


# Funkcja do wyboru poziomu trudności
def choose_difficulty():
    level_to_file = {}
    input_dir = os.path.join(os.getcwd(), "input")
    try:
        for file_name in os.listdir(input_dir):
            if file_name.endswith(".txt"):
                try:
                    file_path = os.path.join(input_dir, file_name)
                    with open(file_path, "r") as file:
                        for line in file:
                            if not line.startswith("#") and line.strip():
                                level_data = line.strip().split(";")
                                if len(level_data) == 3:
                                    level_name = level_data[0]
                                    size, steps = map(int, level_data[1:])
                                    level_to_file[level_name.lower()] = (size, steps)
                except Exception as e:
                    print(f"Nie udało się wczytać pliku {file_name}: {e}")
    except FileNotFoundError:
        print(f"Nie znaleziono folderu {input_dir}. Będziemy używać ustawień domyślnych.")

    print("Dostępne poziomy trudności:")
    for level in level_to_file:
        print(f"- {level}")

    while True:
        print("Podaj poziom trudności, w którym chcesz zagrać:")
        level = input().strip().lower()
        if level in level_to_file:
            size, steps = level_to_file[level]
            return level, (size, steps)
        else:
            print("Nieprawidłowy poziom trudności. Spróbuj ponownie.")


# Funkcja generująca początkową tablicę
def create_puzzle(size):
    side = int(math.sqrt(size))
    puzzle = list(range(1, size)) + [0]
    puzzle_final = [puzzle[i:i + side] for i in range(0, size, side)]
    return puzzle_final


# Funkcja do znajdowania sąsiadów dla zamiany
def search_neighbour(puzzle, i, j, latest):
    n = len(puzzle)
    neighbours = []
    if i > 0: neighbours.append((i - 1, j))  # Górny sąsiad
    if i < n - 1: neighbours.append((i + 1, j))  # Dolny sąsiad
    if j > 0: neighbours.append((i, j - 1))  # Lewy sąsiad
    if j < len(puzzle[i]) - 1: neighbours.append((i, j + 1))  # Prawy sąsiad
    if latest in neighbours:
        neighbours.remove(latest)
    if neighbours:
        selected_coords = random.choice(neighbours)
        return selected_coords
    else:
        print("No neighbours found.")
        return None


# Funkcja do zamieszania tablicy
def shuffle(puzzle, amount):
    latest = None
    for _ in range(amount):
        for i, row in enumerate(puzzle):
            for j, element in enumerate(row):
                if element == 0:
                    to_swap_coords = search_neighbour(puzzle, i, j, latest)
                    if to_swap_coords:
                        ni, nj = to_swap_coords
                        puzzle[i][j], puzzle[ni][nj] = puzzle[ni][nj], puzzle[i][j]
                        latest = (i, j)
                    break


# Funkcja wyświetlająca tablicę w konsoli
def display_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(f"{x:2}" for x in row))
    print()


# Funkcja znajdująca pozycję zera
def find_zero(puzzle):
    for i, row in enumerate(puzzle):
        if 0 in row:
            return i, row.index(0)


# Funkcja do wykonania ruchu
def make_move(puzzle, direction, size_table):
    i, j = find_zero(puzzle)
    if direction == "g" and i > 0:
        puzzle[i][j], puzzle[i - 1][j] = puzzle[i - 1][j], puzzle[i][j]
    elif direction == "d" and i < size_table - 1:
        puzzle[i][j], puzzle[i + 1][j] = puzzle[i + 1][j], puzzle[i][j]
    elif direction == "l" and j > 0:
        puzzle[i][j], puzzle[i][j - 1] = puzzle[i][j - 1], puzzle[i][j]
    elif direction == "p" and j < size_table - 1:
        puzzle[i][j], puzzle[i][j + 1] = puzzle[i][j + 1], puzzle[i][j]
    else:
        print("Nieprawidłowy ruch!")


# Funkcja sprawdzająca, czy tablica jest rozwiązana
def check_solution(puzzle):
    size = len(puzzle) * len(puzzle[0])
    target = list(range(1, size)) + [0]
    puzzle_flat = [num for row in puzzle for num in row]
    return puzzle_flat == target


# Funkcja zapisująca wyniki gry
def save_results(player_name, level, puzzle, moves, time_taken):
    output_dir = os.path.join(os.getcwd(), "output")
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"output_{player_name}_{current_time}.txt"
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{player_name};{level};")
        for i, row in enumerate(puzzle):
            file.write(" ".join(f"{x:2}" for x in row))
            if i != len(puzzle) - 1:
                file.write("/nowa_linia")
        file.write(f";{moves};{time_taken:.2f};{current_time}")
    print(f"Wyniki zostały zapisane do pliku: {file_path}")


# Główna pętla gry
def play_game():
    player_name = get_player_name()
    print(f"Hej {player_name}! Zaczynamy grę...")
    level_name, level_data = choose_difficulty()
    size, steps = level_data

    puzzle = create_puzzle(size)
    shuffle(puzzle, steps)

    while check_solution(puzzle):
        shuffle(puzzle, steps)

    puzzle_to_save = [row[:] for row in puzzle]

    print("Rozwiąż tablicę! Użyj 'g' (góra), 'd' (dół), 'l' (lewo), 'p' (prawo).")
    display_puzzle(puzzle)

    move_count = 0
    start_time = time.time()

    while not check_solution(puzzle):
        move = input("Wykonaj ruch (g/d/l/p) lub wpisz 'quit' aby wyjsc: ").strip().lower()

        if move == "quit":
            print("Zakonczyles gre. Zostaniesz przeniesiony do glownego menu.")
            end_time = time.time()
            duration = end_time - start_time
            save_results(player_name, level_name, puzzle_to_save, "Nie rozwiązano", duration)
            return

        if move in ["g", "d", "l", "p"]:
            make_move(puzzle, move, int(math.sqrt(size)))
            move_count += 1
            display_puzzle(puzzle)
        else:
            print("Nieprawidłowy ruch! Spróbuj jeszcze raz.")

    end_time = time.time()
    duration = end_time - start_time

    print("Gratulacje! Udało ci się rozwiązać tablicę!")
    print(f"Rozwiązałeś tablicę w {duration:.2f} sekund i wykonałeś {move_count} ruchów.")

    save_results(player_name, level_name, puzzle_to_save, move_count, duration)


# Uruchomienie gry
if __name__ == "__main__":
    play_game()
