def broadcast_attack(sio, data):
    """
    Broadcast attack alert to all connected clients
    """

    try:
        print("\n📡 Broadcasting threat alert to all clients...")

        sio.emit("attack_alert", {
            "attacker_ip": data["attacker_ip"],
            "attack_type": data["attack_type"],
            "risk_score": data["risk_score"],
            "attempts": data["attempts"]
        })

        print("✓ Alert sent to clients successfully\n")

    except Exception as e:
        print("Broadcast error:", e)