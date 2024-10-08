import socket
import subprocess
import time
import configparser
import os
import fcntl
client_self_name = subprocess.check_output(
    "ip=$(hostname -I | awk '{print $1}')\n cat /etc/hosts | grep -w $ip | awk '{print $2}'",
    shell=True, text=True
).strip()

def delete_client_section_from_config():
    config = configparser.ConfigParser()

    with open("config1.ini", "r+") as configfile:
        # Lock the file for exclusive access
        fcntl.flock(configfile, fcntl.LOCK_EX)
        
        # Read the config file
        config.read_file(configfile)
        
        # Check if the section [client_self_name] exists, and remove it
        if config.has_section(client_self_name):
            print(f"Deleting section [{client_self_name}] from config1.ini")
            config.remove_section(client_self_name)
            
            # Move the file pointer to the beginning and truncate the file
            configfile.seek(0)
            configfile.truncate()

            # Write the updated config back to the file
            config.write(configfile)
        else:
            print(f"Section [{client_self_name}] not found in config1.ini")
        
        # Unlock the file after the operation
        fcntl.flock(configfile, fcntl.LOCK_UN)

# Perform the deletion once before proceeding with other operations
delete_client_section_from_config()

#with open(f"completed_trans_calculation.txt", 'w') as f:
#        f.write("False")

config = configparser.ConfigParser()


config.read('config1.ini')


hostlist = [host.strip() for host in config.get('hosts', 'hostlist').split(',')]

for server_ip in hostlist:
    if client_self_name != server_ip:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#        for i in range(3):
#            i = int(i) + 1
        server_address = (server_ip, 13897)

        i = 1
        current_time = time.time()

            
        message = f"T1;x;{client_self_name};g*;{i}\x04".encode('utf-8') 
        client_socket.sendto(message, server_address)
        with open(f"time_curr1_{client_self_name}_{i}_{server_ip}.txt", 'w') as f:
            f.write(str(current_time))
        
        client_socket.close()
