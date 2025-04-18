
import subprocess
import os

import subprocess

def allow_remote_port_linux(port):
    """Opens a port using firewall rules in Linux and prints success message."""
    try:
        # Check if UFW is installed
        if subprocess.run(["which", "ufw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            subprocess.run(f"sudo ufw allow {port}/tcp", shell=True, check=True)
            print(f"✅ Port {port} successfully opened using UFW.")
            return True

        # Check if firewalld is installed
        elif subprocess.run(["which", "firewall-cmd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            subprocess.run(f"sudo firewall-cmd --add-port={port}/tcp --permanent", shell=True, check=True)
            subprocess.run("sudo firewall-cmd --reload", shell=True, check=True)
            print(f"✅ Port {port} successfully opened using firewalld.")
            return True

        else:
            # Use iptables as fallback
            subprocess.run(f"sudo iptables -A INPUT -p tcp --dport {port} -j ACCEPT", shell=True, check=True)
            print(f"✅ Port {port} successfully opened using iptables.")
            return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error opening port {port}: {e}")
        return False

# Define paths
# venv_path = "/home/user/project/venv/bin"  # Update with your actual virtual env path
# project_path = "/home/user/project"  # Update with your actual project path

import subprocess
import os

# Define paths
script_name = "Server_Distribute_req.py"
ports = [6000, 6001, 6002, 6003, 6004, 6005]

# Define paths
script_name = "Server_Distribute_req.py"
log_dir = os.path.join(os.getcwd(), "logs")  # Create logs directory in the current working directory

# Ensure log directory exists
os.makedirs(log_dir, exist_ok=True)


for port in ports:

    # Kill any process using this port
    subprocess.run(f"fuser -k {port}/tcp", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



    log_file = os.path.join(log_dir, f"log_file_{port}.log")  # Automatic log file path

    # Create the log file if it doesn't exist
    with open(log_file, "a") as f:
        f.write(f"Starting server on port {port}\n")

    subprocess.Popen(
        f"nohup python {script_name} {port} > {log_file} 2>&1 &",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"🚀 Server script started on port {port}. Check log: {log_file}")

