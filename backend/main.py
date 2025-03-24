from flask import Flask, request, jsonify #request is for getting input values for database
from flask_cors import CORS
import os
import numpy as np
from PIL import Image
import pyodbc #this is for database
import joblib

app=Flask(__name__)
cors = CORS(app, origins='*')

# LOAD PICKLE FILE
def load_joblib_file(filepath):
    try:
        return joblib.load(filepath)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None
    
# FOR PREPROCESSING THE IMAGE FOR PREDICTION
def preprocess_image(image_path):
    img = Image.open(image_path).resize((250, 250))
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    img_flat = img_array.reshape(1, -1)  # Flatten the image
    return img_flat

def results(input):
    if sum(input) >= 2:
        print('Real')
    else:
        print('Fake')

@app.route("/api/text-model", methods=["GET"])
def text_model():
    # LOADING MODELS FROM VERITASIUM AND ALETHEIA
    neural_network = load_joblib_file('models/aletheia_neural_network.pkl')
    random_forest = load_joblib_file('models/aletheia_random_forest.pkl')
    decision_tree = load_joblib_file('models/aletheia_decision_tree.pkl')

    aletheia_names = ['Neural Network', 'Random Forest', 'Decision Tree']
    aletheia_models = [neural_network, random_forest, decision_tree]

    text_data = ["On March 24, 2025, it has been confirmed that Phillippe James Catubig came out as gay, professing his love for his long time friend, Jermanine Pau Malveda."]

    results_text = []
    results_text_json = []
    
    for model in aletheia_models:
        prediction_text = model.predict(text_data)
        label_text = 1 if prediction_text[0] == 'REAL' else 0
        results_text.append(label_text)
        results_text_json.append({'id': aletheia_models.index(model), 'model': aletheia_names[aletheia_models.index(model)], 'prediction': prediction_text[0]})
        print(f'The predicted label for the text {aletheia_names[aletheia_models.index(model)]}: {prediction_text[0]}')

    return jsonify(results_text_json)

@app.route("/api/image-model", methods=["GET"])
def image_model():
    # LOADING MODELS FROM VERITASIUM AND ALETHEIA
    logistic_regression = load_joblib_file('models/veritasium_logistic_regression.pkl')
    passive_aggressive_classifier = load_joblib_file('models/veritasium_passive_aggressive_classifier.pkl')
    svc = load_joblib_file('models/veritasium_svc.pkl')

    # STORE MODELS IN LISTS
    veritasium_names = ['Logistic Regression', 'Passive Aggressive Classifier', 'Support Vector Classifier']
    veritasium_models = [logistic_regression, passive_aggressive_classifier, svc]

    # Path to the image you want to predict
    image_path = r"C:\Users\mat\Downloads\Fake News Image Classifier.v8i.folder\test\fake\568c29f0190000c90178b1d5-260x146_jpeg.rf.4fcbe8ce4797b919a1f771d2e4671a10.jpg"

    # Preprocess the image
    x_image = preprocess_image(image_path)

    results_image = []
    results_image_json = []
   
    # Make a prediction for the image
    for model in veritasium_models:
        prediction_image = model.predict(x_image)
        results_image.append(prediction_image[0])
        label_image = 'real' if prediction_image[0] == 1 else 'fake'
        results_image_json.append({'id': veritasium_models.index(model), 'model': veritasium_names[veritasium_models.index(model)], 'prediction': label_image})
        print(f'The predicted label for the image by {veritasium_names[veritasium_models.index(model)]}: {label_image}')

    return jsonify(results_image_json)

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=.\SQLEXPRESS;"
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
            cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
            if cursor.fetchone():
                return jsonify({"error": "Username already belongs to an account!"}), 400
            
            # Check if the email already exists
            cursor.execute("SELECT * FROM USERS WHERE EMAIL = ?", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email already belongs to an account!"}), 400
            
            cursor.execute("INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", 
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
    is_admin = data.get('isAdmin', False)

    cursor = conn.cursor()
    try:
        if is_admin:
            cursor.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ? AND USER_ID IN (1, 2)", (username, password))
        else:
            cursor.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?", (username, password))

        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid credentials!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        
@app.route('/api/counts', methods=['GET'])
def counts():
    try:
        cursor = conn.cursor()
        
        cursor.execute("""SELECT 
            COUNT(CASE WHEN NEWS_PREDICTION = 'FAKE' AND ADMIN_EVALUATION = 'FALSE' THEN 1 END) AS Fake_False_Count,
            COUNT(CASE WHEN NEWS_PREDICTION = 'FAKE' AND ADMIN_EVALUATION = 'TRUE' THEN 1 END) AS Fake_True_Count,
            COUNT(CASE WHEN NEWS_PREDICTION = 'REAL' AND ADMIN_EVALUATION = 'FALSE' THEN 1 END) AS Real_False_Count,
            COUNT(CASE WHEN NEWS_PREDICTION = 'REAL' AND ADMIN_EVALUATION = 'TRUE' THEN 1 END) AS Real_True_Count FROM RECORDS""")
        counts = cursor.fetchall()

        # Convert records to a list of dictionaries
        counts_list = []
        for row in counts:
            counts_list.append({
                'FalseNegative': row.Fake_False_Count,
                'TrueNegative': row.Fake_True_Count,
                'FalsePositive': row.Real_False_Count,
                'TruePositive': row.Real_True_Count
            })

        return jsonify(counts_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        
@app.route('/api/users', methods=['GET'])
def users():
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT USER_ID, USERNAME, EMAIL FROM USERS")
        users = cursor.fetchall()

        # Convert records to a list of dictionaries
        users_list = []
        for row in users:
            users_list.append({
                'userID': row.USER_ID,
                'username': row.USERNAME,
                'email': row.EMAIL
            })

        return jsonify(users_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()        

@app.route('/api/records', methods=['GET'])
def records():
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM RECORDS")
        records = cursor.fetchall()

        # Convert records to a list of dictionaries
        records_list = []
        for row in records:
            records_list.append({
                'newsId': row.NEWS_ID,
                'userId': row.USER_ID,
                'newsType': row.NEWS_TYPE,
                'newsLink': row.NEWS_LINK,
                'newsPrediction': row.NEWS_PREDICTION,
                'userEvaluation': row.USER_EVALUATION,
                'adminEvaluation': row.ADMIN_EVALUATION,
                'dateOfSubmission': row.SUBMISSION_DATE.strftime('%Y-%m-%d')  # Format date
            })

        return jsonify(records_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        
@app.route('/api/search', methods=['GET'])
def searchrecords():
    search = request.args.get('search', '')
    filter_option = request.args.get('filter', 'All')  # Get the filter option from the request
    cursor = conn.cursor()
    
    # Base query
    query = "SELECT * FROM RECORDS"
    params = []

    # Modify the query based on the selected filter option
    if filter_option == 'UserID':
        query += " WHERE USER_ID LIKE ?"
        params = ['%' + search + '%']
    elif filter_option == 'NewsType':
        query += " WHERE NEWS_TYPE LIKE ?"
        params = ['%' + search + '%']
    elif filter_option == 'All':
        query += " WHERE USER_ID LIKE ? OR NEWS_TYPE LIKE ? OR NEWS_LINK LIKE ? OR NEWS_PREDICTION LIKE ? OR USER_EVALUATION LIKE ? OR ADMIN_EVALUATION LIKE ? OR SUBMISSION_DATE LIKE ?"
        params = ['%' + search + '%'] * 7  # Create a list of parameters for the query

    cursor.execute(query, params)
    records = cursor.fetchall()
    
    # Convert records to a list of dictionaries
    records_list = [{'newsId': r[0], 'userId': r[1], 'newsType': r[2], 'newsLink': r[3], 
                     'newsPrediction': r[4], 'userEvaluation': r[5], 
                     'adminEvaluation': r[6], 'dateOfSubmission': r[7]} for r in records]
    
    cursor.close()
    return jsonify(records_list)

@app.route('/api/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.get_json()
    admin_evaluation = data.get('adminEvaluation')
    
    try:
        cursor = conn.cursor()
        
        # Update the record in the database
        cursor.execute("UPDATE RECORDS SET ADMIN_EVALUATION = ? WHERE NEWS_ID = ?", (admin_evaluation, record_id))
        conn.commit()
        return jsonify({'message': 'Record updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        
if __name__ == "__main__":
    app.run(debug=True, port=8080)