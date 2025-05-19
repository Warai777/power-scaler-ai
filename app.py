from flask import Flask, render_template, request, jsonify, session
from battle_engine import simulate_battle
from gpt_feat_parser import parse_feats_with_gpt
from cache import load_cache, save_cache
from unified_scaling_fetcher import unified_scaling_data
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def home():
    session["chat_history"] = []
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "").strip()

    if not msg:
        return jsonify({"reply": "Please enter a message."})

    msg_lower = msg.lower()

    # Unified scaling fetcher (e.g. "Ichigo full 58 479")
    if " full" in msg_lower:
        try:
            parts = msg.split()
            name = parts[0]
            ep = int(parts[2]) if len(parts) > 2 else None
            ch = int(parts[3]) if len(parts) > 3 else None

            combined = unified_scaling_data(name, episode=ep, chapter=ch)
            reply = parse_feats_with_gpt(combined, f"{name} Composite", 0, source="Unified Scaling")
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"reply": f"❌ Could not parse full profile request: {e}"})

    # Feat parsing
    if "parse:" in msg_lower:
        feat = msg.split("parse:")[1].strip()
        key = f"feat_{feat.replace(' ', '_').lower()}"
        cached = load_cache(key)
        if cached:
            return jsonify({"reply": cached})

        prompt = f"""
You are a power-scaling AI. Extract any feats, stats, hax, or scaling from the following and format them cleanly using markdown.

Feat:
{feat}
"""
        result = parse_feats_with_gpt(prompt, "Feat Parser", 0, source="Manual Feat")
        save_cache(key, result)
        return jsonify({"reply": result})

    # Battle simulation
    elif " vs " in msg_lower:
        try:
            char1, char2 = [x.strip() for x in msg_lower.split(" vs ")]
            result = simulate_battle(char1, char2)
            return jsonify({"reply": result})
        except Exception:
            return jsonify({"reply": "Please use format: 'Character A vs Character B'"})

    # Power-scaling type questions (e.g. how strong is Ichigo)
power_q = re.match(r"how (strong|fast|powerful|durable|haxxed|broken|skilled).*?([a-zA-Z_ ]+)", msg_lower)
if power_q:
    name = power_q.group(2).strip().title()
    try:
        # Pull updated feats + wiki
        data = unified_scaling_data(name)

        # Let GPT format in VS Battle Wiki markdown (with tier overrides)
        reply = parse_feats_with_gpt(
            raw_text=data,
            series_name=name,
            chapter_number=0,
            source="Auto Power Profile",
            wiki_stats={}  # optionally pass wiki stats here if not embedded
        )

        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"reply": f"❌ Could not retrieve profile for {name}: {e}"})

    # Wiki/stat shortcut (e.g. "goku wiki", "luffy stats")
    if any(k in msg_lower for k in [" wiki", " stats"]):
        try:
            name = msg.split()[0].strip().title()
            data = unified_scaling_data(name)
            reply = parse_feats_with_gpt(data, f"{name} Wiki Shortcut", 0, source="Shortcut")
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"reply": f"❌ Could not fetch wiki/stat profile: {e}"})

    # GPT general Q&A (with short memory)
    else:
        history = session.get("chat_history", [])
        prompt = f"""
You are a power-scaling AI assistant.

Instructions:
- Answer in markdown format
- Use bullet points and bold key stats
- Use emojis where appropriate
"""
        for turn in history[-4:]:
            prompt += f"\n{turn['role'].capitalize()}: {turn['content']}"
        prompt += f"\nUser: {msg}\nAssistant:"

        result = parse_feats_with_gpt(prompt, "General Q&A", 0, source="Chat")
        history.append({"role": "user", "content": msg})
        history.append({"role": "assistant", "content": result})
        session["chat_history"] = history

        return jsonify({"reply": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
