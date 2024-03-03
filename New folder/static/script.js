
document.getElementById('proceedBtn').addEventListener('click', function() {
    // Send a request to your Python backend
    // Replace 'backend_url' with the actual URL of your backend endpoint
    fetch('backend_url', {
        method: 'POST', // or 'GET' depending on your backend setup
        headers: {
            'Content-Type': 'application/json'
            // Add any other headers if required
        },
        // You can send data to the backend if needed
        // body: JSON.stringify({/* data object */})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Proceed with whatever you want to do after successful response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
});
