#!/usr/bin/python

import socket
import subprocess
import sys
sys.path.append('/home/nanopi')
from NeoBoardClasses import DifferentialDrive


def quit():
    subprocess.call("killall mjpg_streamer", shell=True)
    socketClient.close()
    socketServer.close()
    sys.exit()


motLA = 7
motLB = 6
motRA = 5
motRB = 4
minSpeed = 15
maxSpeed = 100
wheels = DifferentialDrive(motLA, motLB, motRA, motRB, minSpeed, maxSpeed)

# Start video stream
subprocess.call("/home/nanopi/Programs/FPV/videoStream.sh &", shell=True)

# Create socket
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to any interface, on random un-priviledged port
socketServer.bind(("", 3005))
# Listen up to 1 request
socketServer.listen(1)
print 'Socket started'

while True:
    # Establish connection
    socketClient, address = socketServer.accept()
    print('Client connected')

    while True:
        # Received message must be at most 12 bytes long
        data = socketClient.recv(12)
        if data == 'quit':
            print('Client disconnected')
            # quit()
            break
        angles = data[:-1].split(" ")
        wheels.drive(float(angles[0]), float(angles[1]),0)
