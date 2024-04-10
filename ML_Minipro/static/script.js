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
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => {
      if (data.prediction !== undefined) {
          document.getElementById('result').innerHTML = `<p>Predicted insurance cost: ${data.prediction}</p>`;
      } else {
          throw new Error('Prediction value is undefined');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      document.getElementById('result').innerHTML = `<p>Error: ${error.message}</p>`;
  });
});
