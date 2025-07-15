
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
command_queue = []

@app.route("/api/commands", methods=["GET"])
def pull_command():
    if command_queue:
        return jsonify(command_queue.pop(0))
    return jsonify({"command": "idle"})

@app.route("/api/commands", methods=["POST"])
def push_command():
    cmd = request.get_json(force=True)
    command_queue.append(cmd)
    return jsonify({"status": "queued", "queue_length": len(command_queue)})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "queue_length": len(command_queue)})

def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
