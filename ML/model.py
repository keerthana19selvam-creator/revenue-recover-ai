import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Sample training data
data = {
    "payment_amount": [500, 1000, 1500, 2000, 3000, 5000, 7000, 10000],
    "customer_history": [90, 80, 75, 70, 60, 50, 40, 30],
    "days_overdue": [1, 2, 3, 4, 5, 7, 10, 15],
    "recovery_probability": [95, 90, 85, 80, 72, 60, 45, 30]
}

df = pd.DataFrame(data)

X = df[[
    "payment_amount",
    "customer_history",
    "days_overdue"
]]

y = df["recovery_probability"]

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Save model
joblib.dump(model, "recovery_model.pkl")

print("✅ Recover AI model trained successfully!")
print("✅ Model saved as recovery_model.pkl")