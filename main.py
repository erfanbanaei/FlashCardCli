import sqlite3
import random
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from colorama import Fore, Style

# Connect to the database
conn = sqlite3.connect('words.db')
cursor = conn.cursor()

# Create a table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL UNIQUE,
        correct INTEGER DEFAULT 0,
        incorrect INTEGER DEFAULT 0
    )
''')
conn.commit()

def add_word(word):
    try:
        # Check if the word already exists in the database
        cursor.execute('SELECT id FROM words WHERE word = ?', (word,))
        existing_word = cursor.fetchone()
        if existing_word:
            print(Fore.YELLOW + f'The word "{word}" already exists in the database.' + Style.RESET_ALL)
        else:
            # Add the word to the database
            cursor.execute('INSERT INTO words (word) VALUES (?)', (word,))
            conn.commit()
            print(Fore.GREEN + f'The word "{word}" has been added to the database.' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)

def display_words():
    try:
        # Display all words
        cursor.execute('SELECT id, word FROM words')
        result = cursor.fetchall()
        table = PrettyTable(['ID', 'Word'])
        for row in result:
            table.add_row([row[0], row[1]])
        with open("display_words.txt", "w") as f:
            f.write(f"{table}")
        print(Fore.GREEN + f'Create File (display_words.txt)' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)

def delete_word(word_id):
    try:
        # Delete a word by ID
        cursor.execute('DELETE FROM words WHERE id = ?', (word_id,))
        conn.commit()
        print(Fore.GREEN + f'The word with ID {word_id} has been deleted.' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)

def edit_word(word_id, new_word):
    try:
        # Edit a word by ID
        cursor.execute('UPDATE words SET word = ? WHERE id = ?', (new_word, word_id))
        conn.commit()
        print(Fore.GREEN + f'The word with ID {word_id} has been edited to "{new_word}".' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)

def take_test():
    try:
        # Take a test
        random_words = get_random_words(10)
        print('Random words:')
        for i, word in enumerate(random_words, start=1):
            user_input = input(f'{i}. Do you know the meaning of "{word}"? (yes/no): ')
            if user_input.lower() == 'yes':
                cursor.execute('UPDATE words SET correct = correct + 1 WHERE word = ?', (word,))
            else:
                cursor.execute('UPDATE words SET incorrect = incorrect + 1 WHERE word = ?', (word,))
        conn.commit()
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)

def display_test_results():
    try:
        # Display test results
        cursor.execute('SELECT correct, incorrect FROM words')
        result = cursor.fetchall()
        correct = [row[0] for row in result]
        incorrect = [row[1] for row in result]

        plt.bar(['Correct', 'Incorrect'], [sum(correct), sum(incorrect)], color=['green', 'red'])
        plt.title('Test Results')
        plt.ylabel('Number of Words')
        plt.show()
    except Exception as e:
        print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)

def get_random_words(count):
    # Get a specified number of random words
    cursor.execute('SELECT word FROM words ORDER BY RANDOM() LIMIT ?', (count,))
    result = cursor.fetchall()
    return [row[0] for row in result]

while True:
    # Display the menu
    print(Fore.CYAN + '1. Add Word')
    print('2. Display Words')
    print('3. Delete Word')
    print('4. Edit Word')
    print('5. Take Test')
    print('6. Display Test Results')
    print('7. Exit' + Style.RESET_ALL)

    choice = input(Fore.YELLOW + 'Please enter 1, 2, 3, 4, 5, 6, or 7: ' + Style.RESET_ALL)

    if choice == '1':
        # Add a word
        while True:
            new_word = input('Please enter the word you want to add (or type "done" to exit): ')
            if new_word.lower() == 'done':
                break
            add_word(new_word)
    elif choice == '2':
        # Display all words
        display_words()
    elif choice == '3':
        # Delete a word
        word_id = int(input('Please enter the ID of the word you want to delete: '))
        delete_word(word_id)
    elif choice == '4':
        # Edit a word
        word_id = int(input('Please enter the ID of the word you want to edit: '))
        new_word = input('Please enter the new word: ')
        edit_word(word_id, new_word)
    elif choice == '5':
        # Take a test
        take_test()
    elif choice == '6':
        # Display test results
        display_test_results()
    elif choice == '7':
        # Exit the program
        print(Fore.YELLOW + 'Exiting the program.' + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + 'Invalid input. Please enter 1, 2, 3, 4, 5, 6, or 7.' + Style.RESET_ALL)

# Close the database connection
conn.close()