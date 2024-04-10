from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

app = Flask(__name__)

# Load the insurance dataset
insurance_dataset = pd.read_csv('insurance.csv')

# Preprocess the dataset
insurance_dataset.replace({'sex': {'male': 0, 'female': 1},
                           'smoker': {'yes': 0, 'no': 1},
                           'region': {'southeast': 0, 'southwest': 1, 'northeast': 2, 'northwest': 3}}, inplace=True)

# Create a binary target variable indicating whether the insurance charges are high or not
insurance_dataset['high_charges'] = insurance_dataset['charges'] > insurance_dataset['charges'].median()

# Feature matrix (X) and target vector (y)
X = insurance_dataset.drop(columns=['charges', 'high_charges'], axis=1)
y = insurance_dataset['high_charges']

# One-hot encoding for categorical variables
X_encoded = pd.get_dummies(X)

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=2)

# Model Training
logistic_regressor = LogisticRegression()
logistic_regressor.fit(X_train, y_train)

# Model Evaluation
train_accuracy = logistic_regressor.score(X_train, y_train)
test_accuracy = logistic_regressor.score(X_test, y_test)

print('Training Accuracy: ', train_accuracy)
print('Test Accuracy: ', test_accuracy)


@app.route('/')
def index():
    return render_template('index.html', train_accuracy=train_accuracy, test_accuracy=test_accuracy)


@app.route('/predict', methods=['POST'])
def predict():
    try:
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
        prediction = logistic_regressor.predict(user_input)

        # Log the prediction for debugging
        print('Prediction:', prediction)

        # Return prediction as JSON response
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        # Log any errors that occur during prediction
        print('Prediction Error:', str(e))
        return jsonify({'error': 'An error occurred during prediction.'})

