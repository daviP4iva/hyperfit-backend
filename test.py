import requests

url = "http://localhost:8000/api/v1/chat"
data = {
    "user_message": "¿Cuál es la mejor rutina para ganar músculo?",
    "model": "deepseek/deepseek-chat-v3-0324:free"
}

response = requests.post(url, json=data)
print(response.json())
