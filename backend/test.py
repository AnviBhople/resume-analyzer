import requests

url = "http://127.0.0.1:5000/analyze"

data = {
    "resume": "I know Python and React",
    "job_description": "Looking for Python, React, AWS"
}

response = requests.post(url, json=data)

print(response.json())