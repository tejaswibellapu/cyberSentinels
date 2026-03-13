import sys
sys.stdout.reconfigure(encoding="utf-8")
import socketio
from database.db import init_db, insert_threat
from broadcast import broadcast_attack
from config import SERVER_HOST, SERVER_PORT
# Socket.IO server
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)


# ---------------- CLIENT CONNECT ---------------- #

@sio.event
def connect(sid, environ):
    print(f"[+] Client connected: {sid}")


@sio.event
def disconnect(sid):
    print(f"[-] Client disconnected: {sid}")


# ---------------- RECEIVE ATTACK REPORT ---------------- #

@sio.on("report_attack")
def handle_attack(sid, data):

    print("\n⚠ ATTACK REPORT RECEIVED")
    print("Attacker IP:", data["attacker_ip"])
    print("Attack Type:", data["attack_type"])
    print("Risk Score:", data["risk_score"])
    print("Attempts:", data["attempts"])

    # Store in database
    insert_threat(
        data["attacker_ip"],
        data["attack_type"],
        data["risk_score"],
        data["attempts"]
    )

    # Broadcast to all clients (Durga immunity)
    broadcast_attack(sio, data)

    print("✓ Threat stored and broadcasted\n")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    print("\n🛡 Cyber Autonomous Defense Server Starting...\n")

    # initialize database
    init_db()

    import eventlet
    import eventlet.wsgi

    print(f"Server running on {SERVER_HOST}:{SERVER_PORT}\n")

    eventlet.wsgi.server(
        eventlet.listen((SERVER_HOST, SERVER_PORT)),
        app
    )