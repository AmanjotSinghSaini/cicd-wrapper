from flask import Flask, request, jsonify
import boto3
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the EKS-powered app!"

@app.route("/add", methods=["GET"])
def add():
    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))
    return jsonify({"sum": a + b})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
