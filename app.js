async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('loader');
    const result = document.getElementById('result');
    const urlDisplay = document.getElementById('urlDisplay');

    if (!fileInput.files[0]) {
        alert("Please select a file first.");
        return;
    }

    status.classList.remove('hidden');
    result.classList.add('hidden');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        // Change the URL to your deployed Python backend URL
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.link) {
            status.classList.add('hidden');
            result.classList.remove('hidden');
            urlDisplay.value = data.link;
        } else {
            alert("Upload failed: " + data.error);
            status.classList.add('hidden');
        }
    } catch (error) {
        alert("Could not connect to backend server.");
        status.classList.add('hidden');
    }
}

function copyLink() {
    const urlDisplay = document.getElementById('urlDisplay');
    urlDisplay.select();
    document.execCommand('copy');
    alert("Link copied to clipboard!");
}
