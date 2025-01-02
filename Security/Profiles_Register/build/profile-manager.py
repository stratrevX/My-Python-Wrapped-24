#-----------------------------------------/imports
import sqlite3, platform, os, colorama, time, datetime, pwinput
from colorama import Fore, Style
from datetime import datetime
#-----------------------------------------/objects
script_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(script_dir, 'profiles.db')
conn     = sqlite3.connect(database)
cursor   = conn.cursor()
profile_username = None 
profile_password = None
db_ascii = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣤⣤⣤⣤⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣶⣤⣄⣉⣉⠙⠛⠛⠛⠛⠛⠛⠋⣉⣉⣠⣤⣶⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣄⡉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠛⢉⣠⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣶⣶⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣶⣶⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣶⣤⣈⡉⠛⠛⠻⠿⠿⠿⠿⠿⠿⠟⠛⠛⢉⣁⣤⣶⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠛⠛⠛⠛⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀'''
#-----------------------------------------/functions
def login():
    global profile_password, profile_username
    make_os('clear')
    print(f"{Fore.RED}{db_ascii}{Style.RESET_ALL}")
    cursor.execute('SELECT * FROM register_profile;')
    profile = cursor.fetchall()

    if not profile:
        print("Please create an account.")
        user = input(f"set {Fore.LIGHTYELLOW_EX}username:{Style.RESET_ALL} ").lower().strip()
        pssw = pwinput.pwinput(f"set {Fore.LIGHTYELLOW_EX}password:{Style.RESET_ALL} ", mask='*').lower().strip()
        c_pssw = pwinput.pwinput(f"confirm {Fore.LIGHTYELLOW_EX}password:{Style.RESET_ALL} ", mask='*').lower().strip()

        if pssw != c_pssw:
            print(f"{Fore.RED}Passwords do not match.{Style.RESET_ALL}")
            time.sleep(2)
            login()

        try:
            cursor.execute(
                'INSERT INTO register_profile (id, username, password)'
                'VALUES (?,?,?);',
                (1, user, pssw)
                )
            conn.commit()

            print(f"Profile was made and {Fore.LIGHTGREEN_EX}saved{Style.RESET_ALL} into the database.")
            time.sleep(2)
            home()

        except Exception as e:
            print(f"An {Fore.RED}error{Style.RESET_ALL} occurred trying to save the profile into the database.\nerror_code: {e}.")
            time.sleep(5)

        finally:
            login()
    
    else:
        for value in profile:
            username, profile_username = value[1], value[1]
            password, profile_passowrd = value[2], value[2]

        while True:
            user = input(f"provide {Fore.LIGHTYELLOW_EX}username:{Style.RESET_ALL} ").lower().strip()
            pssw = pwinput.pwinput(f"provide {Fore.LIGHTYELLOW_EX}password:{Style.RESET_ALL} ", mask='*').lower().strip()

            if user == username and pssw == password:
                break

            elif user == 'delete' and pssw == password:
                try:
                    cursor.execute('DELETE FROM register_profile WHERE id = 1;')
                    conn.commit()
                    print(f"the profile was deleted {Fore.GREEN}successfully{Style.RESET_ALL} from the database.")
                    time.sleep(2)
                except Exception as e:
                    print(f"An {Fore.RED}error{Style.RESET_ALL} occurred trying to delete the profile.\n{Fore.RED}error_code: {e}{Style.RESET_ALL}.")
                    time.sleep(5)
                finally:
                    login()
            else:
                if user != username:
                    print(f"{Fore.RED}Incorrect username.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Incorrect password.{Style.RESET_ALL}")

        home()

def home():
    global profile_password, profile_username
    make_os('clear')
    while True:
        query = input(f"1.Extract\n2.Write\n3.Delete\n4.Log_out\n{Fore.LIGHTGREEN_EX}{profile_username}{Style.RESET_ALL}$ ").lower().strip()
        if query in ['1','2','3','4','extract','write','delete','log_out']:
            break
        else:
            print(f"'{query}' is {Fore.RED}not recognized{Style.RESET_ALL} as command.")

    if query in ['1','extract']:
        extract()
    elif query in ['2','write']:
        write()
    elif query in ['3','delete']:
        delete()
    elif query in ['4','log_out']:
        login()

def extract():
    global profile_password, profile_username
    make_os('clear')
    try:
        cursor.execute('SELECT * FROM profiles;')
        profiles = cursor.fetchall()

        if not profiles:
            print(f"{Fore.CYAN}No{Style.RESET_ALL} profile was saved into the database.")
        else:
            for profile in profiles:
                print(f"{Fore.LIGHTYELLOW_EX}ID:{Style.RESET_ALL} {profile[0]}{Style.RESET_ALL}\n{Fore.LIGHTCYAN_EX}service:{Style.RESET_ALL} {profile[1]}\n{Fore.LIGHTCYAN_EX}username:{Style.RESET_ALL} {profile[2]}\n{Fore.LIGHTCYAN_EX}email:{Style.RESET_ALL} {profile[3]}\n{Fore.LIGHTCYAN_EX}password:{Style.RESET_ALL} {profile[4]}\n{Fore.MAGENTA}last updated:{Style.RESET_ALL} {profile[5]}")
                time.sleep(0.5)

            if len(profiles) == 1:
                print(f"One profile was {Fore.GREEN}saved{Style.RESET_ALL} into the database.")
            elif len(profiles) > 1:
                print(f"{len(profiles)} profiles were {Fore.GREEN}saved{Style.RESET_ALL} into the database.")
        
        time.sleep(1)
        hold = input(f"{Fore.CYAN}Press any key to continue.\n{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"An {Fore.RED}error{Style.RESET_ALL} occurred trying to extract data from the database. error_code: {e}")
        time.sleep(5)
    
    finally:
        home()

def write():
    global profile_password, profile_username
    make_os('clear')

    while True:
        iterations = int(input('How many profiles are you saving?\n$'))
        if not isinstance(iterations, int):
            print("Please insert a number.")
            time.sleep(2)
            write()
        else:
            break
    
    for i in range(iterations):
        service   = input('Provide service: ')
        username  = input('Provide profile: ')
        email     = input('Provide email: ')
        password  = input('Provide password: ')
        date      = get_time()  
        
        try:
            cursor.execute("SELECT * FROM profiles;")
            profiles = cursor.fetchall()

            id = len(profiles) + 1

            cursor.execute(
                "INSERT INTO profiles (id, service, username, email, password, last_updated)"
                "VALUES (?,?,?,?,?,?);",
                (id, service, username, email, password, date)
            )

            conn.commit()
            time.sleep(1)
            print(f"This profile was {Fore.GREEN}saved{Style.RESET_ALL} into the database.")
            time.sleep(1)
            hold = input(f"{Fore.CYAN}Press any key to continue.\n{Style.RESET_ALL}")

        except Exception as e:
            print(f"An {Fore.RED}error{Style.RESET_ALL} occurred trying to write data on the database. error_code:{e}")
        
        if (i + 1) == iterations:
            home()

def delete():
    global profile_username, profile_password
    make_os('clear')

    cursor.execute('SELECT * FROM profiles;')
    profiles = cursor.fetchall()

    if not profiles:
        print(f"{Fore.CYAN}No{Style.RESET_ALL} profile was saved into the database.")
        time.sleep(2)
        home()
    
    while True:
        iterations = int(input('How many profiles are you deleting?\n$'))
        if not iterations.isdigit():
            print("Please insert a number.")
            time.sleep(2)
            write()
        else:
            iterations = int(iterations)
            break

    for i in range(iterations):
        profile_id = input("Provide row ID: ")
        try:
            query = 'SELECT * FROM profiles WHERE id = ?;'
            cursor.execute(query, (profile_id,))
            profile = cursor.fetchall()
            if profile:
                query = 'DELETE FROM profiles WHERE id = ?;'
                cursor.execute(query, (profile_id,))
                print(f"The profile number {profile_id} was deleted with {Fore.LIGHTGREEN_EX}success{Style.RESET_ALL}.")
                cursor.execute('SELECT * FROM profiles ORDER BY id')
                profiles = cursor.fetchall()

                for new_id, row in enumerate(profiles, start=1):
                    cursor.execute('UPDATE profiles SET id = ? WHERE id = ?', (new_id, row[0]))

                print("IDs updated.")
            else:
                print("Profile was not found.")
                time.sleep(5)
                home()
            conn.commit()

        except Exception as e:
            print(f"An {Fore.RED}error{Style.RESET_ALL} occurred trying to delete data from the database.\nerror_code: {e}")   
            time.sleep(5)

    home()

def make_os(command):
    if platform.system() == 'Windows':
        if command == 'clear':
            os.system('cls')
    else:
        if command == 'clear':
            os.system('clear')

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#-----------------------------------------/init
if __name__ == '__main__':
    login()
