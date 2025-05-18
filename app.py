from flask import Flask, request, jsonify
from feat_parser import parse_feat
from battle_simulator import simulate_battle

app = Flask(__name__)

@app.route("/")
def home():
    return "Power Scaling AI is Live"

@app.route("/parse", methods=["POST"])
def parse():
    data = request.json
    text = data.get("feat")
    if not text:
        return jsonify({"error": "No feat provided"}), 400
    result = parse_feat(text)
    return jsonify(result)

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.json
    char1 = data.get("char1")
    char2 = data.get("char2")
    result = simulate_battle(char1, char2)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
