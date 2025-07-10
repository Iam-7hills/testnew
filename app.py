from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>IBM ODM API Tester</title>
</head>
<body>
    <h2>IBM ODM REST API Tester</h2>
    <form method="post">
        <label>ODM REST Endpoint URL:</label><br>
        <input type="text" name="odm_url" style="width: 100%%;" placeholder="https://example.com/res/DecisionService/rest/v1/Loan/Eligibility" required><br><br>

        <label>Request JSON:</label><br>
        <textarea name="odm_payload" rows="10" style="width: 100%%;" placeholder='{"applicant": {"age": 30, "income": 75000}}' required></textarea><br><br>

        <button type="submit">Send Request</button>
    </form>

    %s
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result_html = ""

    if request.method == "POST":
        odm_url = request.form.get("odm_url")
        odm_payload = request.form.get("odm_payload")

        try:
            parsed_payload = json.loads(odm_payload)

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.post(odm_url, json=parsed_payload, headers=headers, timeout=10)

            result_html += f"<h3>Response Status: {response.status_code}</h3>"
            result_html += f"<pre>{response.text}</pre>"

        except Exception as e:
            result_html += f"<h3 style='color:red;'>Error</h3><pre>{str(e)}</pre>"

    return HTML_TEMPLATE % result_html

if __name__ == "__main__":
    app.run(debug=True)
