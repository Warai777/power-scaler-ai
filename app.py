from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    session["chat_history"] = []
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "").lower()

    # Feat Parsing
    if "parse" in msg:
        feat = msg.replace("parse", "").strip()
        prompt = f"""
You are a professional feat analysis AI.
Given this feat, extract the power-scaling stats in a structured format.
Respond using clean markdown with labels and bullet points.

### Feat Description:
{feat}

Format like this:
- **Feat Description**:
- **Destructive Capacity**:
- **Speed**:
- **Hax or Abilities Involved**:
- **Scaling Tier (Estimated)**:
- **Summary**:
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    # Battle Simulation
    elif " vs " in msg:
        parts = msg.split("vs")
        char1, char2 = parts[0].strip().title(), parts[1].strip().title()
        prompt = f"""
Simulate a battle between {char1} and {char2}. Format the result as a power-scaling expert.
Include:
- **Win Rate Estimate**
- **Key Strengths**
- **Battle Summary**
- **Final Winner**
Use clean markdown formatting, bullet points, and emoji icons.
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    # Character Profile
    elif "profile" in msg:
        name = msg.replace("profile", "").strip().title()
        prompt = f"""
Provide a power scaling profile for {name}. Include:
- Base Identity
- Powers / Abilities
- Intelligence / Combat Style
- Weaknesses (if any)
- Tier Estimate
Format using markdown tables, bullet points, and emoji-labeled headers.
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    # General GPT conversation
    else:
        history = session.get("chat_history", [])
        prompt = f"""
You are a power-scaling AI. Respond using clean, markdown-formatted bullet points and stats.
Use logic and feats to answer questions accurately.
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
