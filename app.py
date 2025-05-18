from flask import Flask, render_template, request, jsonify, session
from feat_parser import parse_feat
from battle_simulator import simulate_battle
from character_db import get_character_profile, update_character_profile
from openai import OpenAI
from config import OPENAI_API_KEY
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
openai_api_key = OPENAI_API_KEY
client = OpenAI(api_key=openai_api_key)

@app.route("/")
def home():
    session["chat_history"] = []
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "").lower()

    if "parse" in msg or "feat" in msg:
        feat = msg.replace("parse", "").replace("feat", "").strip()
       prompt = f"""You are a power-scaling AI. Parse and extract the key stats from the following feat in a clean, readable format.

Instructions:
- Use bullet points
- Bold important terms (e.g., **Speed**, **Tier**, etc.)
- End with a short summary

Feat:
{feat}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    elif "vs" in msg or "win" in msg:
        parts = msg.replace("who wins", "").split("vs")
        if len(parts) == 2:
            char1, char2 = parts[0].strip(), parts[1].strip()
            prompt = f"""
You are a battle simulation AI. Simulate a fight between {char1} and {char2} based on feats, logic, and power scaling.

Instructions:
- Use bolded headers (e.g., **Winner**, **Win Rate**, **Key Advantages**, **Battle Summary**)
- Make it look like a clean, ranked breakdown
- Respond in bullet points or short paragraphs
"""
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            reply = response.choices[0].message.content
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": "Please use format: 'Character A vs Character B'"})

    elif "profile" in msg:
        char = msg.replace("profile", "").strip()
        profile = get_character_profile(char)
        return jsonify({"reply": profile})

    else:
        history = session.get("chat_history", [])
        prompt = f"""
You are a power-scaling AI assistant.

Instructions:
- Always format your replies clearly using bullet points or short sections
- Bold key stats and terms (e.g., **Speed**, **Tier**, **Abilities**)
- Answer concisely and intelligently based on previous context

Conversation history:
"""
        for turn in history[-5:]:
            prompt += f"\n{turn['role'].capitalize()}: {turn['content']}"
        prompt += f"\nUser: {msg}\nAssistant:"

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        reply = response.choices[0].message.content
        history.append({"role": "user", "content": msg})
        history.append({"role": "assistant", "content": reply})
        session["chat_history"] = history
        return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
