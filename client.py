import requests
import json
import time
response = requests.post('http://localhost:5000/generate', json={
    "prompt": "Once upon a time in a land far, far away,",
    "max_length": 80
})

if response.status_code == 200:
    print("Response from server:")
    print(response.json())
else:
    print("Error:", response.status_code)
    print("Response:", response.text)