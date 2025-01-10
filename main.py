from Server.server import start_server
from Client.client import start_client

def main():
    while True:
        print("Welcome to Silentious!")
        print("1. Start as Server")
        print("2. Start as Client")
        
        choice = input("Choose an option (1/2): ")

        if choice == "1":
            print("Starting the server...")
            start_server()  # Start the server
            break
        elif choice == "2":
            print("Starting the client...")
            start_client()  # Start the client
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()