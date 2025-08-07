from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '*****',
    'database': 'voterdb'
}

# Function to connect to MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to fetch all registrations
@app.route('/registrations', methods=['GET'])
def get_registrations():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT name, email, phone, aadhaar, dob, gender, address, city, state, pincode 
                FROM registrations
            """)
            results = cursor.fetchall()
            return jsonify(results)
        except Error as e:
            print(f"❌ Error fetching data: {e}")
            return jsonify({"error": "Failed to fetch data from database."}), 500
        finally:
            cursor.close()
            connection.close()
    return jsonify({"error": "Failed to connect to the database."}), 500

# Route to display and handle registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            aadhaar = request.form['aadhaar']
            dob = request.form['dob']
            gender = request.form['gender']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            pincode = request.form['pincode']

            # Log form data for debugging
            print(f"Received data: {name}, {email}, {phone}, {aadhaar}, {dob}, {gender}, {address}, {city}, {state}, {pincode}")

            # Insert into database
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                insert_query = """
                    INSERT INTO registrations 
                    (name, email, phone, aadhaar, dob, gender, address, city, state, pincode)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (name, email, phone, aadhaar, dob, gender, address, city, state, pincode))
                connection.commit()

                # Return success response
                return jsonify({"message": "✅ Registration submitted successfully!"}), 201
        except Error as e:
            # Log specific error for debugging
            print(f"❌ Error during registration: {e}")
            return jsonify({"error": f"There was an error while submitting the registration: {e}"}), 500
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return render_template('reg.html')  # For GET requests

# Run the app
if __name__ == '__main__':
    print("Registered Routes:", app.url_map)
    app.run(debug=True)

