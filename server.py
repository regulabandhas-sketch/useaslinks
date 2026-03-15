from flask import Flask,request,jsonify
import base64,requests,json,random,string

app=Flask(__name__)

TOKEN="YOUR_GITHUB_TOKEN"
REPO="USERNAME/REPO"

def short_id():

 return ''.join(random.choices(string.ascii_letters+string.digits,k=6))

@app.route("/upload",methods=["POST"])
def upload():

 file=request.files["file"]

 # simple virus safety
 if file.filename.endswith(".exe"):
  return jsonify({"error":"blocked file type"})

 name=file.filename

 content=base64.b64encode(file.read()).decode()

 url=f"https://api.github.com/repos/{REPO}/contents/uploads/{name}"

 headers={"Authorization":f"token {TOKEN}"}

 data={"message":"upload","content":content}

 requests.put(url,json=data,headers=headers)

 link=f"https://raw.githubusercontent.com/{REPO}/main/uploads/{name}"

 short=short_id()

 with open("files.json") as f:
  db=json.load(f)

 db["files"].append({
  "name":name,
  "url":link,
  "short":short
 })

 with open("files.json","w") as f:
  json.dump(db,f,indent=2)

 return jsonify({"url":link,"short":short})

@app.route("/files")
def files():

 with open("files.json") as f:
  return jsonify(json.load(f))

app.run(port=5000)
