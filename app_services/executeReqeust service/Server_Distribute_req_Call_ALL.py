import subprocess
import os

# ------------ for windoes

import subprocess

def allow_remote_port_windows(port):
    command = (
        f'netsh advfirewall firewall add rule name="Flask App {port}" '
        f'dir=in action=allow protocol=TCP localport={port} remoteip=any'
    )
    subprocess.run(command, shell=True, check=True)

# # #-- for server 130
# venv_path = r'C:\Users\Administrator\SepehrSmart\SepehrSmart\.venv\Scripts'
# project_path = r'C:\Users\Administrator\SepehrSmart\SepehrSmart'


# # #-- for server 45
venv_path = r'C:\Users\Administrator\PycharmProjects\web\vn\Scripts'
project_path = r'C:\Users\Administrator\Desktop\SepehrSmart_services'


#--Distribute_req (6000,6001,6002)
script_name = 'Server_Distribute_req.py'
ports = [6000, 6001, 6002,6003,6004,6005]
for port in ports:
    allow_remote_port_windows(port)
    subprocess.Popen(
                f'start cmd /k "cd /d {venv_path} && activate && cd /d {project_path} && python {script_name} {port}"',
                     shell=True)

    # #--- for server 185
    # subprocess.Popen(
    #             f'start cmd /k "python {script_name} {port}"',
    #                  shell=True)


