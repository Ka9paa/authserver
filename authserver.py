from flask import Flask, request, jsonify
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load secret API key from .env
API_KEY = os.getenv("AUTH_HEADER")  # ✅ Must match .env variable name
print("Loaded API_KEY from env:", API_KEY)  # ✅ Put this right here

# In-memory key store (use DB in production)
license_keys = {}

# Middleware to require API key in header
def require_api_key(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route("/api/generate", methods=["POST"])
@require_api_key
def generate_key():
    new_key = secrets.token_hex(16)
    license_keys[new_key] = {"valid": True}
    return jsonify({"key": new_key})

@app.route("/api/verify", methods=["POST"])
def verify_key():
    data = request.get_json()
    key = data.get("key")

    if not key or key not in license_keys:
        return jsonify({"valid": False, "error": "Invalid key"}), 400

    if license_keys[key]["valid"]:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False, "error": "Revoked"}), 403

@app.route("/")
def home():
    return "✅ Key Auth Server Running"

if __name__ == "__main__":
    app.run(debug=True)
