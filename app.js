async function uploadFile(){

let file=document.getElementById("file").files[0]

if(!file){
alert("Select file")
return
}

/* Preview */

let preview=document.getElementById("preview")

if(file.type.startsWith("image")){
preview.innerHTML=`<img src="${URL.createObjectURL(file)}">`
}

if(file.type.startsWith("video")){
preview.innerHTML=`<video controls src="${URL.createObjectURL(file)}"></video>`
}

/* Upload */

let data=new FormData()
data.append("file",file)

let xhr=new XMLHttpRequest()

xhr.upload.onprogress=function(e){

let percent=(e.loaded/e.total)*100

document.getElementById("bar").style.width=percent+"%"

}

xhr.onload=function(){

let res=JSON.parse(xhr.responseText)

alert("Link: "+res.short)

loadFiles()

}

xhr.open("POST","http://127.0.0.1:5000/upload")

xhr.send(data)

}

/* Load file manager */

async function loadFiles(){

let res=await fetch("http://127.0.0.1:5000/files")

let data=await res.json()

let html=""

data.files.forEach(f=>{

html+=`
<div class="file">
<b>${f.name}</b><br>
<a href="${f.url}" target="_blank">Download</a><br>
Short: ${f.short}
</div>
`

})

document.getElementById("files").innerHTML=html

}

loadFiles()
