import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import joblib

print("Step 1: starting")

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="@hen2001",
    database="agriculture_project",
    connection_timeout=5,
    use_pure=True
)

print("Step 2: connected")

query = "SELECT * FROM crop_recommendation"
data = pd.read_sql(query, con=connection)

print("Step 3: data loaded")

X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

print("Step 4: X and y created")
print("X shape:", X.shape)
print("y shape:", y.shape)
print(X.head())
print(y.head())

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("Step 5: train-test split done")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model trained successfully")
print("Accuracy:", accuracy)

joblib.dump(model, "crop_model.pkl")
print("Model saved successfully")

loaded_model = joblib.load("crop_model.pkl")
sample_data = [[90, 42, 43, 20.8, 82.0, 6.5, 202.9]]

prediction = loaded_model.predict(sample_data)

print("Predicted crop:", prediction[0])

report = classification_report(y_test, y_pred)

print("Classification Report:")
print(report)

connection.close()
print("Step 6: done")