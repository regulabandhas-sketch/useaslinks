let API="https://your-backend.onrender.com"

function login(){

let u=document.getElementById("user").value
let p=document.getElementById("pass").value

if(u==="admin" && p==="1234"){

document.getElementById("loginBox").style.display="none"
document.getElementById("app").style.display="block"

loadFiles()

}else{

alert("wrong login")

}

}

/* drag drop */

let dropzone=document.getElementById("dropzone")

dropzone.ondragover=e=>{
e.preventDefault()
}

dropzone.ondrop=e=>{
e.preventDefault()
uploadFile(e.dataTransfer.files[0])
}

/* upload */

function upload(){

let file=document.getElementById("file").files[0]

uploadFile(file)

}

function uploadFile(file){

let preview=document.getElementById("preview")

if(file.type.startsWith("image")){

preview.innerHTML=`<img width=300 src="${URL.createObjectURL(file)}">`

}

if(file.type.startsWith("video")){

preview.innerHTML=`<video width=400 controls src="${URL.createObjectURL(file)}"></video>`

}

let data=new FormData()

data.append("file",file)

let xhr=new XMLHttpRequest()

xhr.upload.onprogress=e=>{

let p=(e.loaded/e.total)*100

document.getElementById("bar").style.width=p+"%"

}

xhr.onload=()=>{

alert("Uploaded")

loadFiles()

}

xhr.open("POST",API+"/upload")

xhr.send(data)

}

/* file manager */

async function loadFiles(){

let r=await fetch(API+"/files")

let d=await r.json()

let html=""

d.files.forEach(f=>{

html+=`
<div class="file">
<b>${f.name}</b><br>
<a href="${f.url}" target="_blank">Download</a>
</div>
`

})

document.getElementById("files").innerHTML=html

}
