from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# LOAD ML MODEL
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ML", "recovery_model.pkl")

model = None

try:
    model = joblib.load(MODEL_PATH)
    print("✅ ML model loaded successfully!")
    print("Model:", type(model))
    print("Model path:", MODEL_PATH)
except Exception as e:
    print("❌ ML model loading failed!")
    print("Error:", e)


# --------------------------------------------------
# SAMPLE PAYMENT DATA
# --------------------------------------------------

payments = [
    {
        "id": "PAY001",
        "customer": "Arun",
        "amount": 2500,
        "status": "Failed",
        "recovery_probability": 85,
        "recommended_action": "Retry payment"
    },
    {
        "id": "PAY002",
        "customer": "Priya",
        "amount": 5000,
        "status": "Pending",
        "recovery_probability": 72,
        "recommended_action": "Send smart reminder"
    },
    {
        "id": "PAY003",
        "customer": "Rahul",
        "amount": 1200,
        "status": "Failed",
        "recovery_probability": 40,
        "recommended_action": "Offer alternative payment method"
    }
]


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Recover AI Backend is Running!",
        "status": "online"
    })


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })


# --------------------------------------------------
# GET PAYMENTS
# --------------------------------------------------

@app.route("/payments", methods=["GET"])
def get_payments():
    return jsonify(payments)


# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

@app.route("/analytics", methods=["GET"])
def analytics():

    total_payments = len(payments)

    failed_payments = sum(
        1 for payment in payments
        if payment["status"] == "Failed"
    )

    pending_payments = sum(
        1 for payment in payments
        if payment["status"] == "Pending"
    )

    total_amount = sum(
        payment["amount"]
        for payment in payments
    )

    average_probability = round(
        sum(
            payment["recovery_probability"]
            for payment in payments
        ) / total_payments
    )

    return jsonify({
        "total_payments": total_payments,
        "failed_payments": failed_payments,
        "pending_payments": pending_payments,
        "total_amount": total_amount,
        "average_recovery_probability": average_probability
    })


# --------------------------------------------------
# AI PREDICTION
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return jsonify({
            "success": False,
            "error": "ML model could not be loaded"
        }), 500

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        features = data.get("features")

        if features is None:
            return jsonify({
                "success": False,
                "error": "Please provide 'features'"
            }), 400

        # ML prediction
        prediction = model.predict([features])

        result = prediction[0]

        if hasattr(result, "item"):
            result = result.item()

        return jsonify({
            "success": True,
            "prediction": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":

    print("----------------------------------------")
    print("        RECOVER AI BACKEND")
    print("----------------------------------------")
    print("Server starting...")
    print("URL: http://127.0.0.1:5000")
    print("Health: http://127.0.0.1:5000/health")
    print("Payments: http://127.0.0.1:5000/payments")
    print("Analytics: http://127.0.0.1:5000/analytics")
    print("----------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )