from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your existing DSVW security lab and AI proxy
DSVW_URL = "http://localhost:65412"
AI_PROXY = "http://localhost:8118/generate"   # adjust if needed

challenges = [
    {"id": 1, "name": "SQL Injection", "url": f"{DSVW_URL}/sqli/", "hint": "Try ' OR 1=1 --"},
    {"id": 2, "name": "XSS", "url": f"{DSVW_URL}/xss/", "hint": "Inject <script>alert(1)</script>"},
    {"id": 3, "name": "Command Injection", "url": f"{DSVW_URL}/cmd/", "hint": "Try ; ls"},
]

scores = {}

@app.route('/challenges', methods=['GET'])
def get_challenges():
    return jsonify(challenges)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    cid = data.get('challenge_id')
    answer = data.get('answer', '')
    user = data.get('user', 'anon')

    valid = False
    if cid == 1 and ("' OR" in answer or "UNION" in answer):
        valid = True
    elif cid == 2 and ("<script>" in answer or "alert" in answer):
        valid = True
    elif cid == 3 and (";" in answer or "&&" in answer):
        valid = True

    if valid:
        scores[user] = scores.get(user, 0) + 10
        msg = "✅ Correct! +10 points"
    else:
        # Use AI to generate a hint (optional)
        try:
            hint_resp = requests.post(AI_PROXY, json={"prompt": f"Give a hint for challenge {cid} with answer: {answer}"}, timeout=3)
            hint = hint_resp.json().get('response', 'Try harder!')
        except:
            hint = "Try harder!"
        msg = f"❌ Incorrect. Hint: {hint}"

    return jsonify({"message": msg, "score": scores.get(user, 0)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089)
