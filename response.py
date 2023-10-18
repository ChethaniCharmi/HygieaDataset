# Import necessary libraries
import requests

# URL of your Flask app
url = 'http://127.0.0.1:5000/predict'

# Input data as a dictionary (change this to your data)
data = {'file': ('image.jpg', open('image.jpg', 'rb'))}

# Send a POST request
response = requests.post(url, files=data)

# Check the response
if response.status_code == 200:
    predictions = response.json()
    print("Predictions:")
    for i, probability in enumerate(predictions):
        print(f"Class {i + 1}: {probability:.4f}")
    max_probability = max(predictions)
    predicted_class = predictions.index(max_probability) + 1  # Add 1 to make it 1-based if classes are 1, 2, 3, ...
    print(f"Predicted Class: {predicted_class}")
else:
    print("Error:", response.status_code, response.text)
