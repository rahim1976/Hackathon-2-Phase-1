import subprocess
import time
import httpx
import sys
import os
from todo_cli.client.base import DAEMON_URL

def is_daemon_running() -> bool:
    try:
        response = httpx.get(f"{DAEMON_URL}/daemon/status", timeout=0.1)
        return response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException):
        return False

def start_daemon():
    if is_daemon_running():
        return

    # Using sys.executable to ensure we use the same Python environment
    # Running uvicorn as a subprocess
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "todo_cli.daemon.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        start_new_session=True
    )

    # Wait for daemon to start
    retries = 50
    while retries > 0:
        if is_daemon_running():
            return
        time.sleep(0.1)
        retries -= 1

    print("Error: Failed to start background daemon.", file=sys.stderr)
    sys.exit(1)

def ensure_daemon():
    if not is_daemon_running():
        start_daemon()
