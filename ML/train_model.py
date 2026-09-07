import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Sample recovery data
data = {
    "failed_transactions": [2, 5, 8, 1, 10, 6, 3, 12, 4, 7],
    "avg_amount": [500, 1200, 2000, 300, 2500, 1500, 700, 3000, 900, 1800],
    "retry_count": [1, 2, 4, 1, 5, 3, 1, 6, 2, 3],
    "recovery_time": [2, 5, 8, 1, 10, 7, 3, 12, 4, 6]
}

df = pd.DataFrame(data)

# Features and target
X = df[["failed_transactions", "avg_amount", "retry_count"]]
y = df["recovery_time"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, "recovery_model.pkl")

print("AI Recovery Prediction Model trained successfully!")
print("Model saved as recovery_model.pkl")