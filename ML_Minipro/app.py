from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained logistic regression model
with open('trained_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract user input from the form
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    bmi = float(request.form['bmi'])
    children = int(request.form['children'])
    smoker = int(request.form['smoker'])
    region = int(request.form['region'])

    # Create a DataFrame from the user input
    user_input = pd.DataFrame({'age': [age], 'sex': [sex], 'bmi': [bmi],
                               'children': [children], 'smoker': [smoker], 'region': [region]})

    # Make prediction using the trained model
    prediction = model.predict(user_input)

    # Return prediction as JSON response
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
