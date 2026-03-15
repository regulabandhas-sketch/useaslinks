from flask import Flask,request,jsonify
import os,json

app=Flask(__name__)

UPLOAD="uploads"

if not os.path.exists(UPLOAD):
 os.mkdir(UPLOAD)

DB="files.json"

if not os.path.exists(DB):
 open(DB,"w").write('{"files":[]}')

@app.route("/upload",methods=["POST"])
def upload():

 file=request.files["file"]

 path=os.path.join(UPLOAD,file.filename)

 file.save(path)

 url="/file/"+file.filename

 db=json.load(open(DB))

 db["files"].append({
  "name":file.filename,
  "url":url
 })

 json.dump(db,open(DB,"w"),indent=2)

 return {"ok":True}

@app.route("/files")
def files():

 return json.load(open(DB))

@app.route("/file/<name>")
def file(name):

 return app.send_static_file("uploads/"+name)

app.run()
