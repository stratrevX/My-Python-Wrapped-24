#----------------------------------------------------------------/imports
import os, socket, threading, colorama, time, datetime, requests, platform
from datetime import datetime
from colorama import Fore, Style
#----------------------------------------------------------------/objects
server_ip        = requests.get("https://api.ipify.org").text.strip()
code_proc        = None
conn_list        = []
clients_lock     = threading.Lock()
requested_comm   = None
requested_action = None
os_name          = platform.system()
#----------------------------------------------------------------/functions
def run_server():
    global code_proc, server_ip, requested_action, requested_comm
    requested_comm = 'clear'
    get_os()

    if not code_proc:
        requested_action = 'input'
        proc_status = input(f"{get_time()} {get_action()} Set {Fore.LIGHTMAGENTA_EX}Key protection?{Style.RESET_ALL} (y/n)\n")
        if proc_status.lower() == 'y':
            requested_action = 'input'
            code_proc = input(f"{get_time()} {get_action()} Set key: ")
    
    requested_action = 'info'
    print(f"{get_time()} {get_action()} Checking port {Fore.LIGHTMAGENTA_EX}443{Style.RESET_ALL}")
    
    if not check_port():
        requested_action = 'warn'
        print(f"{get_time()} {get_action()} Port {Fore.LIGHTMAGENTA_EX}443{Style.RESET_ALL} may not be open or it's already used.")
        time.sleep(0.5)
        requested_action = 'input'
        request = input(f"{get_time()} {get_action()} Do you want to continue? (y/n)\n")
        if request == 'n':
            return
    else:
        requested_action = 'info'
        print(f"{get_time()} {get_action()} Port {Fore.LIGHTMAGENTA_EX}443{Style.RESET_ALL} is open.")
        time.sleep(0.5)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0',443))
    server_socket.listen(5)

    requested_action = 'info'
    requested_comm   = 'clear'
    get_os()
    
    print(f"{get_time()} {get_action()} Now listening on every direction on port {Fore.LIGHTMAGENTA_EX}443{Style.RESET_ALL}.")
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def handle_client(conn, addr):
    global code_proc, requested_action
    requested_action = 'warn'
    print(f"{get_time()} {get_action()} Someone is trying to establish connection with us.")

    with clients_lock:
        conn_list.append(conn)
    
    conn.sendall(f"{get_time()} {get_action()} You are trying to establish connection with a ByteSpeak server.".encode())

    if code_proc:
        conn.sendall(f"{get_time()} {get_action()} Please, provide the key to access: ".encode())
        key = conn.recv(1024).decode().strip()
        if key != code_proc:
            requested_action = 'warn'
            conn.sendall(f"{get_time()} {get_action()} You didn't provide the correct key, closing the conn.".encode())
            print(f"{get_time()} {get_action()} {Fore.LIGHTMAGENTA_EX}{addr}{Style.RESET_ALL} didn't provide the correct key, closing the conn with the client.")
            time.sleep(2)
            conn.close()
            return
        else:
            requested_action = 'info'
            conn.sendall(f"{get_time()} {get_action()} You provided the correct key, access allowed.".encode())
            print(f"{get_time()} {get_action()} The client was able to provide the correct key.")

    conn.sendall(f"{get_time()} {get_action()} Please set an username: ".encode())
    client_id = conn.recv(1024).decode().strip()
    time.sleep(2)

    threading.Thread(target=recv_texts, args=(conn, addr, client_id), daemon=True).start()

def broadcast_texts(text, sender_conn):
    global requested_action, requested_comm
    with clients_lock:
        for conn in conn_list:
            try:
                if conn != sender_conn:
                    conn.sendall(text.encode())
            except Exception as e:
                requested_action = 'warn'
                print(f"{get_time()} {get_action()} Error broadcasting: {e}")

def recv_texts(conn, addr, client_id):
    global requested_action
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                requested_action = 'warn'
                print(f"{get_time()} {get_action()} Connection with {client_id} was lost.")
                break
            print(f"{get_time()} Received from {client_id}: {data}")

            text = f"{get_time()} prompted by {client_id}: {data}"
            broadcast_texts(text, conn)
        
        except ConnectionResetError:
            requested_action = 'warn'
            print(f"{get_time()} {get_action()} Connection with {client_id} was forcibly closed.")
            break
        
        except Exception as e:
            requested_action = 'warn'
            print(f"{get_time()} {get_action()} Error receiving text from {client_id}: {e}")
            break

    with clients_lock:
        conn_list.remove(conn)
    conn.close()

def check_port():
    try:
        with socket.create_connection((server_ip,443), timeout=3):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

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
run_server()