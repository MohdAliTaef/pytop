import paramiko
from influxdb import InfluxDBClient
import json
import sys
import logging
import datetime, threading, time

argv = sys.argv
hostname = argv[1]
port = argv[2]
username = argv[3]
password = argv[4]
n = int(argv[5])


client = InfluxDBClient('localhost', 8086, 'root', 'root')
client.create_database('centos_top')
client.switch_database('centos_top')


s = paramiko.SSHClient()
s.load_system_host_keys()
s.connect(hostname, port, username, password)


def interval():
    next_call = time.time()
    while True:
        
        command = "top -n 1 -b | grep Tasks | awk '{print $2\"|\"$4\"|\"$6\"|\"$8\"|\"$10}' && date -u +%s"
        (stdin, stdout, stderr) = s.exec_command(command,get_pty=True)

        output = []
       
        for line in stdout.readlines():
            output.append(line)
  
        array = output[0].split("|")
        total = int(array[0])
        running = int(array[1])
        sleeping = int(array[2])
        stopped = int(array[3])
        zombie = int(array[4])

        json_body = [
            {
                "measurement": "centos_processes",
                "tags": {
                    "ip": hostname
                },
                "fields": {
                    "total": total,
                    "running":running,
                    "sleeping":sleeping,
                    "stopped":stopped,
                    "zombie":zombie
                }
            }
        ]
        client.write_points(json_body )

        
        next_call = next_call+n;
        time.sleep(next_call - time.time())

timerThread = threading.Thread(target=interval)
timerThread.daemon = True
timerThread.start()
interval()

s.close()
exit




    
