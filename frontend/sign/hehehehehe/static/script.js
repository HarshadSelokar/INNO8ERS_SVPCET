const socket = io();

function startRecognition() {
    document.getElementById("result").innerText = "Listening...";
    document.getElementById("images").innerHTML = "";
    document.getElementById("microphone").style.display = "inline"; // Show mic animation

    socket.emit('start_recognition');
}

socket.on('listening', function(data) {
    if (!data.status) {
        document.getElementById("microphone").style.display = "none"; // Hide mic
    }
});

socket.on('display_results', function(data) {
    let resultDiv = document.getElementById('result');
    let imagesDiv = document.getElementById('images');
    
    resultDiv.innerText = "Recognized Text: " + data.text;
    imagesDiv.innerHTML = ''; // Clear previous images

    data.images.forEach(img => {
        let imageElement = document.createElement('img');
        imageElement.src = img;
        imageElement.style.marginRight = "10px"; // Space between letters
        imagesDiv.appendChild(imageElement);
    });
});

socket.on('error', function(data) {
    document.getElementById("result").innerText = data.message;
});
