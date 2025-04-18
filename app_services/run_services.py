import os
import platform
import subprocess

def is_windows():
    return platform.system().lower() == "windows"

def create_command(file_name, port):
    if is_windows():
        return f'start cmd /k "python {file_name} --port {port}"'
    else:
        return f'gnome-terminal -- bash -c "python {file_name} --port {port}; exec bash"'

def run_services():
    # Define services with their ports
    services = [
        ('"Booking service\\Booking_Hotel_flask_OK.py"', 5001),
        # ('"Jimbo services\\Jimbo_Hotel_flask_OK.py"', 5002),
        ('"Alaedin service\\Crawl_alaedin_Rooms_Flask_OK.py"', 5003),
        ('"Snapp service\\Crawl_Snapp_SignIn_OK.py"', 5004),
        ('"Eghamat24 service\\Eghamat24_Service_OK.py"', 8022)
    ]

    # Create commands based on the operating system
    if is_windows():
        # For Windows, use netsh to allow ports through firewall
        for _, port in services:
            firewall_command = f'netsh advfirewall firewall add rule name="Open Port {port}" dir=in action=allow protocol=TCP localport={port}'
            subprocess.run(firewall_command, shell=True)
    else:
        # For Linux, use ufw to allow ports through firewall
        for _, port in services:
            firewall_command = f'sudo ufw allow {port}/tcp'
            subprocess.run(firewall_command, shell=True)

    # Start each service in a new window
    for file_name, port in services:
        command = create_command(file_name, port)
        os.system(command)

if __name__ == "__main__":
    print("Starting services...")
    run_services()
    print("All services have been started.")