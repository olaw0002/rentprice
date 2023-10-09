from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to the database
conn = mysql.connector.connect(
    host="tp06-dev.mysql.database.azure.com",
    user="tp06",
    password='pN7X8SefeLpAW1IxFK7g',
    database="property"
)
cursor = conn.cursor()

@app.route('/')
def index():
    # Fetch suburbs from the database
    cursor.execute("SELECT DISTINCT Suburb FROM housingprices")
    suburbs = [row[0] for row in cursor.fetchall()]

    # Define housing types
    housing_types = ['`1 bedroom flat`', '`2 bedroom flat`', '`3 bedroom flat`', '`2 bedroom house`', '`3 bedroom house`', '`4 bedroom house`']

    return render_template('index.html', suburbs=suburbs, housing_types=housing_types)

@app.route('/get_prices', methods=['POST'])
def get_prices():
    selected_suburb = request.form['suburb']
    selected_housing_type = request.form['housing_type']

    # Fetch the price from the database using parameterized query
    cursor.execute("SELECT {} FROM housingprices WHERE Suburb = %s".format(selected_housing_type), (selected_suburb,))
    result = cursor.fetchone()

    if result:
        price = result[0]
    else:
        price = "Price not available"

    return render_template('result.html', suburb=selected_suburb, housing_type=selected_housing_type, price=price)

if __name__ == '__main__':
    app.run(debug=True)
