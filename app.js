async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('statusArea');
    const result = document.getElementById('resultArea');
    const urlDisplay = document.getElementById('urlDisplay');

    if (!fileInput.files[0]) return alert("Select a file first!");

    // Show loading, hide result
    status.classList.remove('hidden');
    result.classList.add('hidden');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (data.link) {
            status.classList.add('hidden');
            result.classList.remove('hidden');
            urlDisplay.value = data.link; // This displays the professional link
        }
    } catch (e) {
        alert("Backend not connected!");
        status.classList.add('hidden');
    }
}

function copyLink() {
    const copyText = document.getElementById("urlDisplay");
    copyText.select();
    document.execCommand("copy");
    alert("Link Copied!");
}
