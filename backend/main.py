from flask import Flask, request, jsonify #request is for getting input values for database
from flask_cors import CORS
import os
import numpy as np
from PIL import Image
import pyodbc #this is for database
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app=Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/api/algo", methods=["GET"])
def algo():
    # Path to the dataset
    dataset_path = r"C:\Users\mat\Documents\4TH YEAR\veritasium\-CODE-\backend\train"

    # Initialize lists for images and labels
    images = []
    labels = []

    # Iterate through 'fake' and 'real' folders
    for label in ['fake', 'real']:
        folder_path = os.path.join(dataset_path, label)
        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            try:
                # Load the image and resize to a fixed size (e.g., 64x64)
                img = Image.open(img_path).resize((64, 64))
                img_array = np.array(img)  # Convert image to a NumPy array
                images.append(img_array)  # Append image data
                labels.append(label)      # Append label
            except Exception as e:
                print(f"Error loading {img_path}: {e}")

    # Convert lists to NumPy arrays
    X = np.array(images)
    y = np.array([1 if label == 'real' else 0 for label in labels])  # Convert labels to binary (1 for 'real', 0 for 'fake')

    # Normalize pixel values to [0, 1]
    X = X / 255.0

    # Flatten images (if using traditional ML models)
    X_flat = X.reshape(X.shape[0], -1)

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_flat, y, test_size=0.2, random_state=42)

    # Define models
    models = [
        LogisticRegression(solver='liblinear')
    ]
    
    results = []

    # Train and evaluate each model
    for i in models:
        reg = i.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred) * 100
        
        results.append({"model_name": reg.__class__.__name__, "prediction": "real" if y_pred[0] == 1 else "fake", "accuracy": accuracy})
        
    return jsonify(results)

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-FQOOPV8\SQLEXPRESS;"
    "DATABASE=Thesis;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(conn_str)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['name']
    email = data['email']
    password = data['password']
    
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()    
            # Check if the username already exists
            cursor.execute("SELECT * FROM [USER] WHERE USERNAME = ?", (username,))
            if cursor.fetchone():
                return jsonify({"error": "Username already belongs to an account!"}), 400
            
            # Check if the email already exists
            cursor.execute("SELECT * FROM [USER] WHERE EMAIL = ?", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email already belongs to an account!"}), 400
            
            cursor.execute("INSERT INTO [USER] (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", 
                        (username, email, password))
            conn.commit()
            return jsonify({"message": "Account creation successful!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['name']
    password = data['password']

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM [USER] WHERE USERNAME = ? AND PASSWORD = ?", (username, password))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid credentials!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        
if __name__ == "__main__":
    app.run(debug=True, port=8080)