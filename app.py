from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #e0f7fa, #fff);
                color: #2c3e50;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                font-size: 3em;
                margin: 0;
            }
            p {
                font-size: 1.2em;
                color: #555;
            }
            footer {
                position: absolute;
                bottom: 20px;
                font-size: 0.9em;
                color: #888;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to My Website</h1>
        <p>Clean. Simple. Elegant.</p>
        <footer>© Amanjot Singh Saini</footer>
    </body>
    </html>
    """

# Functional but hidden API (not shown in UI)
@app.route("/add", methods=["GET"])
def add():
    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))
    return jsonify({"sum": a + b})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
