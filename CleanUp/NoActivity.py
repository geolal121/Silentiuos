import time
import os
from CheckPID import CheckPID
from CleanUp import CleanUp

class NoActivityMonitor:
    def __init__(self, timeout=300, all_clients=None, server_socket=None):
        self.timeout = timeout
        self.last_activity = time.time()
        self.running = True
        self.all_clients = all_clients if all_clients else []
        self.server_socket = server_socket

    def update_activity(self):
        self.last_activity = time.time()

    def monitor_activity(self):
        while self.running:
            if time.time() - self.last_activity > self.timeout:
                self.shutdown_due_to_inactivity()
            time.sleep(1)

    def shutdown_due_to_inactivity(self):
        print("[NoActivityMonitor]: No activity detected. Shutting down...")
        CleanUp.clear_terminal()
        CleanUp.clean_resources(self.all_clients, self.server_socket)
        current_pid = os.getpid()
        all_pids = CheckPID.list_running_pids()
        for pid in all_pids:
            if pid != current_pid:  # Avoid killing the monitor itself
                CheckPID.terminate_pid(pid)
        os._exit(0)

    def start_monitoring(self):
        self.monitor_activity()

    def stop_monitoring(self):
        self.running = False

# Example Usage
if __name__ == "__main__":
    all_clients = []  # Example: List of active clients
    server_socket = None  # Example: Server socket
    monitor = NoActivityMonitor(timeout=300, all_clients=all_clients, server_socket=server_socket)

    try:
        while True:
            user_input = input("Type something (or leave idle to trigger timeout): ")
            if user_input.lower() == "exit":
                monitor.stop_monitoring()
                CleanUp.clean_resources(all_clients, server_socket)
                print("[NoActivityMonitor]: Exiting...")
                break
            monitor.update_activity()
    except KeyboardInterrupt:
        monitor.stop_monitoring()
        CleanUp.clean_resources(all_clients, server_socket)
        print("\n[NoActivityMonitor]: Program interrupted. Exiting...")
