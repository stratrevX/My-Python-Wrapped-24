#---------------------------------#imports
import random, time, colorama, os, sqlite3, datetime, platform
from colorama import Fore, Style
from datetime import datetime
#---------------------------------#objects
script_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(script_dir, 'passwords.db')
conn     = sqlite3.connect(database)
cursor   = conn.cursor()
text_ascii = '''
 _______                                                                        __         ______                                                     __                         
|       \                                                                      |  \       /      \                                                   |  \                        
| $$$$$$$\ ______    _______   _______  __   __   __   ______    ______    ____| $$      |  $$$$$$\  ______   _______    ______    ______   ______  _| $$_     ______    ______  
| $$__/ $$|      \  /       \ /       \|  \ |  \ |  \ /      \  /      \  /      $$      | $$ __\$$ /      \ |       \  /      \  /      \ |      \|   $$ \   /      \  /      \ 
| $$    $$ \$$$$$$\|  $$$$$$$|  $$$$$$$| $$ | $$ | $$|  $$$$$$\|  $$$$$$\|  $$$$$$$      | $$|    \|  $$$$$$\| $$$$$$$\|  $$$$$$\|  $$$$$$\ \$$$$$$\\$$$$$$  |  $$$$$$\|  $$$$$$\\
| $$$$$$$ /      $$ \$$    \  \$$    \ | $$ | $$ | $$| $$  | $$| $$   \$$| $$  | $$      | $$ \$$$$| $$    $$| $$  | $$| $$    $$| $$   \$$/      $$ | $$ __ | $$  | $$| $$   \$$
| $$     |  $$$$$$$ _\$$$$$$\ _\$$$$$$\| $$_/ $$_/ $$| $$__/ $$| $$      | $$__| $$      | $$__| $$| $$$$$$$$| $$  | $$| $$$$$$$$| $$     |  $$$$$$$ | $$|  \| $$__/ $$| $$      
| $$      \$$    $$|       $$|       $$ \$$   $$   $$ \$$    $$| $$       \$$    $$       \$$    $$ \$$     \| $$  | $$ \$$     \| $$      \$$    $$  \$$  $$ \$$    $$| $$      
 \$$       \$$$$$$$ \$$$$$$$  \$$$$$$$   \$$$$$\$$$$   \$$$$$$  \$$        \$$$$$$$        \$$$$$$   \$$$$$$$ \$$   \$$  \$$$$$$$ \$$       \$$$$$$$   \$$$$   \$$$$$$  \$$      
                                                                                                                                                                                 
                                                                                                                                                                                 
                                                                                                                                                                                 
'''
#---------------------------------#functions
def init():
    make_os('clear')
    print(f"{Fore.RED}{text_ascii}{Style.RESET_ALL}")
    time.sleep(2)
    request = input("1. generate_passwords\n2. Exit\n$ ").lower().strip()
    if request in ['1', 'generate_passwords']:
        generator()
    elif request in ['2', 'exit']:
        time.sleep(2)
        exit()

def generator():
    make_os('clear')
    iterations = int(input("How many passwords do you want to generate?\n$ "))
    prefix = 'setupyourprefix='

    for i in range(iterations):
        password = prefix + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+', k=12))
        time.sleep(0.5)
        print(f"{Fore.BLUE}generated password{Style.RESET_ALL}: {password}")    
        try:
            cursor.execute('SELECT * FROM generated_passwords;')
            passwords = cursor.fetchall()
            date = get_time()

            cursor.execute(
                'INSERT INTO generated_passwords (id, password, generated)'
                'VALUES (?,?,?);',
                ((len(passwords) + 1), password, date)
                )
            conn.commit()
            print(f"Password was {Fore.LIGHTGREEN_EX}saved{Style.RESET_ALL} into the database.")

        except Exception as e:
            print(f"An {Fore.RED}error{Style.RESET_ALL} occurred trying to save the password into the database.\nerror_code: {e}.")

    time.sleep(2)
    hold = input("Press enter to continue...")
    init()

def make_os(command):
    if platform.system() == 'Windows':
        if command == 'clear':
            os.system('cls')
    else:
        if command == 'clear':
            os.system('clear')

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#---------------------------------#init
if __name__ == '__main__':
    init()