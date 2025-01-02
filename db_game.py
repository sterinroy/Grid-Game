import random
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect('db_game.db')
    cursor = conn.cursor()

    # Create table to store grid elements
    cursor.execute('''CREATE TABLE IF NOT EXISTS grid (
        x INTEGER,
        y INTEGER,
        element TEXT
    )''')

    # Create table to store player information
    cursor.execute('''CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        x INTEGER,
        y INTEGER,
        score INTEGER
    )''')

    conn.commit()
    conn.close()

# Initialize the grid in the database
def initialize_grid():
    conn = sqlite3.connect('db_game.db')
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute('DELETE FROM grid')

    # Populate the grid with elements
    for _ in range(20):
        x, y = random.randint(0, 9), random.randint(0, 9)
        cursor.execute('INSERT INTO grid (x, y, element) VALUES (?, ?, ?)', (x, y, 'R'))

    for _ in range(10):
        x, y = random.randint(0, 9), random.randint(0, 9)
        cursor.execute('INSERT INTO grid (x, y, element) VALUES (?, ?, ?)', (x, y, 'X'))

    for _ in range(5):
        x, y = random.randint(0, 9), random.randint(0, 9)
        cursor.execute('INSERT INTO grid (x, y, element) VALUES (?, ?, ?)', (x, y, 'I'))

    conn.commit()
    conn.close()

# Initialize player in the database
def initialize_player():
    conn = sqlite3.connect('db_game.db')
    cursor = conn.cursor()

    # Clear existing player data
    cursor.execute('DELETE FROM player')

    # Set starting position and score
    cursor.execute('INSERT INTO player (x, y, score) VALUES (?, ?, ?)', (5, 5, 0))

    conn.commit()
    conn.close()

# Print the grid
def print_grid():
    conn = sqlite3.connect('db_game.db')
    cursor = conn.cursor()

    # Fetch grid data
    grid_data = cursor.execute('SELECT x, y, element FROM grid').fetchall()
    player_data = cursor.execute('SELECT x, y FROM player').fetchone()

    # Generate grid
    grid = [["." for _ in range(10)] for _ in range(10)]
    for x, y, element in grid_data:
        grid[x][y] = element

    px, py = player_data
    grid[px][py] = '*'

    for row in grid:
        print(" ".join(row))

    conn.close()

# Move the player
def move_player(direction):
    conn = sqlite3.connect('db_game.db')
    cursor = conn.cursor()

    # Get current player position and score
    player_data = cursor.execute('SELECT x, y, score FROM player').fetchone()
    px, py, score = player_data

    # Update position based on direction
    if direction == 'w' and px > 0:
        px -= 1
    elif direction == 's' and px < 9:
        px += 1
    elif direction == 'a' and py > 0:
        py -= 1
    elif direction == 'd' and py < 9:
        py += 1

    # Check grid element at the new position
    element = cursor.execute('SELECT element FROM grid WHERE x = ? AND y = ?', (px, py)).fetchone()

    if element:
        if element[0] == 'X':
            print("You hit corrupted data! Game over.")
            conn.close()
            return False
        elif element[0] == 'R':
            score += 10
            cursor.execute('DELETE FROM grid WHERE x = ? AND y = ?', (px, py))
        elif element[0] == 'I':
            score += 5
            cursor.execute('DELETE FROM grid WHERE x = ? AND y = ?', (px, py))

    # Update player position and score
    cursor.execute('UPDATE player SET x = ?, y = ?, score = ?', (px, py, score))

    conn.commit()
    conn.close()
    return True

# Main game logic
def play_game():
    setup_database()
    initialize_grid()
    initialize_player()

    while True:
        print_grid()
        conn = sqlite3.connect('db_game.db')
        cursor = conn.cursor()
        score = cursor.execute('SELECT score FROM player').fetchone()[0]
        conn.close()

        print(f"Score: {score}")
        print("Move using W (up), A (left), S (down), D (right). Type 'q' to quit.")
        move = input("Your move: ").lower()

        if move == 'q':
            print("Thanks for playing!")
            break

        if not move_player(move):
            break

# Run the game
if __name__ == "__main__":
    play_game()
