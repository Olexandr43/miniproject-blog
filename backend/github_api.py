import os
import requests
from fastapi import HTTPException
import base64

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

def create_github_file(repo: str, path: str, content: str):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_info = response.json()
        sha = file_info['sha']
    else:
        sha = None

    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {
        "message": "Create or update file",
        "content": encoded_content,
    }

    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [201, 200]:
        return {"message": "File created or updated successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
