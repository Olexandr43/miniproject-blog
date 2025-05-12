import os
import requests
from fastapi import HTTPException
import base64

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Ваш токен доступу
GITHUB_API_URL = "https://api.github.com"

def create_github_file(repo: str, path: str, content: str):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Кодуємо вміст у Base64
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {
        "message": "Create file",
        "content": encoded_content  # Використовуємо закодований вміст
    }
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return {"message": "File created successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
