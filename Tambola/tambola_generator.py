import sqlite3
import random

def create_database():
    conn = sqlite3.connect('tambola.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
                 id INTEGER PRIMARY KEY,
                 numbers TEXT
                 )''')
    conn.commit()
    conn.close()

def generate_ticket():
    ticket = [[0] * 9 for _ in range(3)]  # Initialize ticket with zeros
    nums = random.sample(range(1, 91), 15)  # Generate 15 unique numbers
    nums.sort()
    col_indices = [i for i in range(9)]
    for num in nums:
        col = num // 10 if num % 10 == 0 else num // 10 + 1
        row = col_indices[col - 1]
        ticket[row // 3][col - 1] = num
        col_indices[col - 1] += 1
    return ticket

def save_tickets(num_sets):
    conn = sqlite3.connect('tambola.db')
    c = conn.cursor()
    for _ in range(num_sets):
        for _ in range(6):  # Generate 6 tickets per set
            ticket = generate_ticket()
            while True:
                c.execute('SELECT * FROM tickets WHERE numbers = ?', ['|'.join(map(str, row)) for row in ticket])
                if not c.fetchone():
                    break
                ticket = generate_ticket()
            c.execute('INSERT INTO tickets (numbers) VALUES (?)', ['|'.join(map(str, row)) for row in ticket])
    conn.commit()
    conn.close()

if __name__ == "__main__":
    num_sets = int(input("Enter the number of sets: "))
    create_database()
    save_tickets(num_sets)
    print(f"{num_sets} sets of Tambola tickets generated and saved successfully.")
