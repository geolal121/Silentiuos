import os
import signal

class CheckPID:
    @staticmethod
    def is_pid_running(pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    @staticmethod
    def list_running_pids():
        return [int(pid) for pid in os.listdir('/proc') if pid.isdigit()]

    @staticmethod
    def terminate_pid(pid):
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"[CheckPID]: PID {pid} terminated.")
        except Exception as e:
            print(f"[CheckPID]: Could not terminate PID {pid}: {e}")