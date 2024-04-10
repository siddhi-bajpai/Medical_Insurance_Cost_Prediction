document.getElementById('predictionForm').addEventListener('submit', function(event) {
    event.preventDefault();
   
    const formData = new FormData(this);
   
    fetch('/predict', {
      method: 'POST',
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('result').innerHTML = `<p>Predicted insurance cost: ${data.prediction}</p>`;
    })
    .catch(error => console.error('Error:', error));
});
