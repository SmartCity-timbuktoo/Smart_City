
import subprocess
import time
import signal
import sys
import os
import requests

# Configuration
CITIZEN_APP_PORT = 8501
ADMIN_APP_PORT = 8502
HOST = "localhost"

# ANSI Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"

processes = []

def log(msg, color=RESET):
    print(f"{color}[SYSTEM] {msg}{RESET}")

def check_port(port):
    """Check if a port is responding."""
    try:
        response = requests.get(f"http://{HOST}:{port}/_stcore/health")
        return response.status_code == 200
    except:
        return False

def wait_for_service(port, name, timeout=30):
    """Wait for a service to become healthy."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_port(port):
            log(f"{name} is ONLINE at http://{HOST}:{port}", GREEN)
            return True
        time.sleep(1)
    log(f"{name} failed to start on port {port}", RED)
    return False

def cleanup(signum, frame):
    """Graceful shutdown handler."""
    log("\nShutting down services...", index=RED)
    for p in processes:
        if os.name == 'nt':
            # Windows requires stronger kill signal for subprocess groups
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)])
        else:
            p.terminate()
            
    log("All services stopped. Goodbye!", CYAN)
    sys.exit(0)

def main():
    log("Initializing Addis-Sync Multi-App System...", CYAN)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # 1. Launch Citizen App
    log(f"Launching Citizen Interface on Port {CITIZEN_APP_PORT}...")
    citizen_cmd = [
        "uv", "run", "streamlit", "run", "app.py",
        "--server.port", str(CITIZEN_APP_PORT),
        "--server.headless", "true"
    ]
    p1 = subprocess.Popen(citizen_cmd, cwd=os.getcwd())
    processes.append(p1)

    # 2. Launch Admin App
    log(f"Launching Admin Dashboard on Port {ADMIN_APP_PORT}...")
    admin_cmd = [
        "uv", "run", "streamlit", "run", "admin_worker_app.py",
        "--server.port", str(ADMIN_APP_PORT),
        "--server.headless", "true"
    ]
    p2 = subprocess.Popen(admin_cmd, cwd=os.getcwd())
    processes.append(p2)

    # 3. Health Checks
    log("Waiting for services to initialize...")
    c_ready = wait_for_service(CITIZEN_APP_PORT, "Citizen App")
    a_ready = wait_for_service(ADMIN_APP_PORT, "Admin Dashboard")

    if c_ready and a_ready:
        log("\n✅ SYSTEM OPERATIONAL", GREEN)
        log(f"🌍 Citizen App:  http://{HOST}:{CITIZEN_APP_PORT}", GREEN)
        log(f"🛠️  Admin Panel:  http://{HOST}:{ADMIN_APP_PORT}", GREEN)
        log("\nPress Ctrl+C to stop all services.")
        
        # Keep main thread alive
        while True:
            time.sleep(1)
    else:
        log("System startup FAILED. Check logs.", RED)
        cleanup(None, None)

if __name__ == "__main__":
    main()
