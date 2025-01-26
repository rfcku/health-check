from flask import Flask, jsonify
import threading
from kafka import Kafka

app = Flask(__name__)
kafka = Kafka() 

@app.route("/check_health", methods=["GET"])
def get_latest_health_check():
    if not kafka.messages:
        return jsonify({"message": "No health statuses available yet."}), 200
    return jsonify(kafka.get_messages()), 200



@app.route("/get_latest_health_check", methods=["GET"])
def check_health():
    if not kafka.messages:  
        return jsonify({"message": "No health statuses available yet"}), 200
    return jsonify(kafka.get_latest_messages()), 200

if __name__ == "__main__":
    
    threading.Thread(target=kafka.consume, daemon=True).start()
    app.run(host="0.0.0.0", port=9001, debug=True)

