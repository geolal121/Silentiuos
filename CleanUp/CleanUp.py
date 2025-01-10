import os
import signal

class CleanUp:
    @staticmethod
    def clean_resources(all_clients, server_socket=None):
        print("[CleanUp]: Cleaning up resources...")
        for client in all_clients:
            client.close()
        if server_socket:
            server_socket.close()
        print("[CleanUp]: All sockets closed.")

    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def terminate_process(pid):
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"[CleanUp]: Process {pid} terminated.")
        except Exception as e:
            print(f"[CleanUp]: Could not terminate process {pid}: {e}")
