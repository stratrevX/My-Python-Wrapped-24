#----------------------------------------------------------------/imports
import os, time, socket, threading, colorama, datetime, platform
from colorama import Fore, Style
from datetime import datetime
#----------------------------------------------------------------/objects
requested_comm   = None
requested_action = None
os_name          = platform.system()
#----------------------------------------------------------------/functions
def run_client():
    global requested_action, requested_comm
    
    requested_comm = 'clear'
    get_os()

    requested_action = 'input'
    ip   = input(f"{get_time()} {get_action()} Provide IP: ")
    requested_action = 'input'
    port = int(input(f"{get_time()} {get_action()} Provide Port: "))
    requested_action = 'info'

    print(f"{get_time()} {get_action()} Establishing connection with {Fore.LIGHTMAGENTA_EX}{ip}{Style.RESET_ALL}.")
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_sock.connect((ip, port))
        requested_action = 'info'
        print(f"{get_time()} {get_action()} Established connection with {ip}")
        requested_comm = 'clear'
        get_os()
        threading.Thread(target=recv_text, args=(client_sock,), daemon=True).start()

    except Exception as e:
        requested_action = 'warn'
        print(f"{get_time()} {get_action()} Connection error: {e}")
        time.sleep(2)
        return
    
    interval = time.time()
    while True:
        try:
            ct = time.time()
            if ct - interval >= 3:
                text = input("\n>")
                if text.lower() == 'break':
                    client_sock.close()
                    return

                client_sock.sendall(text.encode())
                interval = ct
            else:
                wait_time = 3 - int(ct - interval)
                print(f"{get_time()} {get_action()} Wait {wait_time} seconds before sending another text.", end='\r', flush=True)
                time.sleep(1)

        except KeyboardInterrupt:
            client_sock.close()
            return
        
        except Exception as e:
            requested_action = 'warn'
            print(f"{get_time()} {get_action()} Error:\n{e}")
            client_sock.close()
            time.sleep(2)
            return
        
def recv_text(client_sock):
    global requested_action, requested_comm
    while True:
        try:
            data = client_sock.recv(1024).decode()
            if not data:
                requested_action = 'warn'
                print(f"{get_time()} {get_action()} Connection closed by the server.\n Closing the client.")
                time.sleep(2)
                client_sock.close()
                return
            print(f"{get_time()} {get_action()} Server: {data}")
        except Exception as e:
            requested_action = 'warn'
            print(f"{get_time()} {get_action()} An error occurred while receiving data:\n{e}")
            time.sleep(2)
            client_sock.close()
            return
        
def get_action():
    global requested_action
    if requested_action == "info":
        return f"{Fore.LIGHTBLUE_EX}[i]{Style.RESET_ALL}"
    elif requested_action == "warn":
        return f"{Fore.LIGHTBLUE_EX}[!]{Style.RESET_ALL}"
    elif requested_action == "input":
        return f"{Fore.LIGHTBLUE_EX}[>]{Style.RESET_ALL}"

def get_os():
    global requested_comm
    if requested_comm == 'clear':
        if os_name == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
        requested_comm = None

def get_time():
    return datetime.now().strftime(f"{Fore.LIGHTMAGENTA_EX}%H{Style.RESET_ALL}:{Fore.LIGHTMAGENTA_EX}%M{Style.RESET_ALL}:{Fore.LIGHTMAGENTA_EX}%S{Style.RESET_ALL}")




#----------------------------------------------------------------/initialize
run_client()