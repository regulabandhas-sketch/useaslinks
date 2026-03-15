from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import uuid # For generating unique, professional IDs
import os

app = Flask(__name__)
CORS(app)

# Configuration
GITHUB_TOKEN = "your_github_token"
REPO_OWNER = "your_username"
REPO_NAME = "storage"
CUSTOM_DOMAIN = "useas.online" # Your domain name

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    file_extension = os.path.splitext(file.filename)[1]
    
    # Generate a professional short ID like krakenfiles (e.g., f8k2j9)
    short_id = str(uuid.uuid4())[:8]
    new_filename = f"{short_id}{file_extension}"
    
    encoded_content = base64.b64encode(file.read()).decode('utf-8')
    
    # GitHub API Path
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/f/{new_filename}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"Permanent upload: {new_filename}",
        "content": encoded_content
    }

    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code in [200, 201]:
        # Professional Link Format
        # Option A: Using your domain
        professional_link = f"https://{CUSTOM_DOMAIN}/f/{new_filename}"
        
        # Option B: Direct GitHub Pages link (if you enable Pages on the repo)
        # professional_link = f"https://{REPO_OWNER}.github.io/{REPO_NAME}/f/{new_filename}"
        
        return jsonify({
            "status": "success",
            "link": professional_link,
            "file_name": file.filename,
            "size": "Stored Permanently"
        })
    
    return jsonify({"error": "Upload failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
