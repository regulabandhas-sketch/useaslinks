from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app)

# Configuration - Keep these secure!
GITHUB_TOKEN = "your_github_personal_access_token"
REPO_OWNER = "your_username"
REPO_NAME = "your_storage_repo"
BRANCH = "main"

@app.route('/upload', methods=['POST'])
def upload_to_github():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    file_content = file.read()
    
    # Encode file to Base64 for GitHub API
    encoded_content = base64.b64encode(file_content).decode('utf-8')
    
    # Create a unique path for the file
    file_path = f"uploads/{file.filename}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"Upload {file.filename}",
        "content": encoded_content,
        "branch": BRANCH
    }

    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code in [200, 201]:
        # Generate the permanent raw link
        raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{file_path}"
        return jsonify({"link": raw_url, "status": "success"})
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)
