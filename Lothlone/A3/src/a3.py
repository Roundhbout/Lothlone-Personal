#!/usr/bin/env python3

import socket
import subprocess
import os

# Open socket, bind to port 8000, set to listen for and accept connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 8000))
    sock.listen()
    conn, addr = sock.accept()

    # Receive bytes into d, decode d and append to data, break when '\nEND' is received
    with conn:
        print('Connected: ', addr)
        data = ''
        while True:
            d = conn.recv(1024)
            data += d.decode()
            if not d or '\nEND' in data:
                break

        # Remove whitespace, slice off 'END', re-encode data for subprocess
        data = "".join(data.split())
        data = data[:-3]
        data = data.encode()

        # Get absolute path to a2.py
        pth = os.getcwd() + "\\a2.py"
        pth = pth.replace("\\", "/")
        
        # Create subprocess running a2.py --sum, set stdin to be data
        output = subprocess.run(pth + " --sum", input=data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Catch any errors returned by a2.py
        try:
            output.check_returncode()
        except subprocess.CalledProcessError:
            print("a2.py returned error {} from input, please try again".format(output.returncode))

        # Send output back across connection
        print(output)
        conn.sendall(output.stdout)
