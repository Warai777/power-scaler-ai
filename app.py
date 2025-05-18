from flask import Flask, render_template, request, jsonify
from feat_parser import parse_feat
from battle_simulator import simulate_battle
from character_db import get_character_profile, update_character_profile
from openai import OpenAI
from config import OPENAI_API_KEY
import os

app = Flask(__name__)
openai_api_key = OPENAI_API_KEY

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "").lower()

    if "parse" in msg or "feat" in msg:
        feat = msg.replace("parse", "").replace("feat", "").strip()
        result = parse_feat(feat)
        return jsonify({"reply": result.get("parsed", "Failed to parse feat.")})

    elif "vs" in msg or "win" in msg:
        parts = msg.replace("who wins", "").split("vs")
        if len(parts) == 2:
            char1, char2 = parts[0].strip(), parts[1].strip()
            result = simulate_battle(char1, char2)
            return jsonify({"reply": result.get("result", "Could not simulate battle.")})
        else:
            return jsonify({"reply": "Please use format: 'Character A vs Character B'"})

    elif "profile" in msg:
        char = msg.replace("profile", "").strip()
        profile = get_character_profile(char)
        return jsonify({"reply": profile})

    else:
        prompt = f"This user said: {msg}. Interpret this as a power-scaling request and respond intelligently."
        client = OpenAI(api_key=openai_api_key)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
