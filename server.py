import os
import json
from flask import Flask, request, jsonify, send_from_directory
from google import genai
from google.genai import types

# ── Configuration ──────────────────────────────────────────
# API key is read from environment variable (set in Render dashboard)
# Never hardcode your key in production!
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCkUXlyV0MkZcL5A4Pcq8a6Ea5GW9VERec")
PORT    = int(os.environ.get("PORT", 8000))

client = genai.Client(api_key=API_KEY)
app    = Flask(__name__, static_folder=".", static_url_path="")

# ── AI Classification ──────────────────────────────────────
def generate_ai_content(user_text):
    system_prompt = (
        "You are an expert AI assistant for a fake news detection website. "
        "Analyze the given news text carefully and determine if it is Real News or Fake News. "
        "Consider: factual accuracy, sensationalism, misleading language, logical consistency, and known facts. "
        "Respond ONLY with a valid JSON object — no markdown, no extra text — in this exact format:\n"
        '{"labels": ["Real News"], "scores": [0.92], "reason": "Short explanation here."}\n'
        "OR if fake:\n"
        '{"labels": ["Fake News"], "scores": [0.88], "reason": "Short explanation here."}\n'
        "The score must be between 0.5 and 1.0 reflecting your confidence. Be smart and accurate."
    )

    full_prompt = f"{system_prompt}\n\nNews text to analyze:\n{user_text}"

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

# ── Routes ─────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        res = jsonify({})
        res.headers["Access-Control-Allow-Origin"]  = "*"
        res.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        res.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return res

    try:
        user_text = request.json.get("inputs", "").strip()
        if not user_text:
            return jsonify({"error": "No text provided."}), 400

        print(f"Analyzing: {user_text[:80]}...")
        result = generate_ai_content(user_text)
        print(f"Result: {result.get('labels', ['?'])[0]}")
        return jsonify(result)

    except Exception as e:
        err = str(e)
        print(f"ERROR: {err}")

        friendly = "System Error. Check your API key."
        if "429" in err:
            friendly = "Rate limit reached. Please wait 1 minute and try again."
        elif "404" in err:
            friendly = "Model not available in your region."
        elif "API_KEY_INVALID" in err or "400" in err:
            friendly = "Invalid API Key."

        return jsonify({"error": friendly, "details": err}), 500

# ── Run ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
