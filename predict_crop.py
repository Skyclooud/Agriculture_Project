
import joblib

loaded_model = joblib.load("crop_model.pkl")

N = float(input("Enter Nitrogen value: "))
P = float(input("Enter Phosphorus value: "))
K = float(input("Enter Potassium value: "))
temperature = float(input("Enter temperature value: "))
humidity = float(input("Enter humidity value: "))
ph = float(input("Enter pH value: "))
rainfall = float(input("Enter rainfall value: "))

sample_data = [[N, P, K, temperature, humidity, ph, rainfall]]

prediction = loaded_model.predict(sample_data)

print("Predicted crop is:", prediction[0])