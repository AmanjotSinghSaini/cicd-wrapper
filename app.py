from flask import Flask

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
                background: linear-gradient(135deg, #0f0f0f, #1c1c1c);
                color: #ffffff;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 10px;
            }
            p {
                font-size: 1.3em;
                margin-top: 0;
            }
            .neon {
                color: #39ff14; /* Neon green */
                font-weight: bold;
                font-family: monospace;
                margin-top: 10px;
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
        <h1>Welcome to the Webpage</h1>
        <p>This website was deployed via CI/CD Pipeline built by</p>
        <div class="neon">https://github.com/AmanjotSinghSaini</div>
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
