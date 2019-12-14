# Server for the project
# server_proj2.py
# basic server with DB, no web interface yet.
#################################################################

# flask related
from flask import Flask, jsonify, request, abort

#https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object/39257479
# Price is a decimal in the DB
# pip install simplejson
from decimal import Decimal

# For interaction with MySQL Table = food in Database = datarepresentation
from zfoodDAO import foodDAO

app = Flask(__name__, static_url_path='', static_folder='.')

##################################################################
# List of foods (or a DB)
# Price is a decimal(6,2) xxxx.xx in dDB
""" foods=[
    {"id": 1, "category": "dairy", "name":"cheese", "price": 2.50},
    {"id": 2, "category": "vegetable","name":"carrots", "price:": 1.10},
    {"id": 3, "category": "meat","name":"steak", "price:": 6.75},
    {"id": 4, "category": "canned","name":"peas", "price:": 1.25}   
] """

##################################################################
# Maybe have another array for second table like a cart?
cart=[
    {"id": 1, "name":"chedder", "amount": 2},
    {"id": 2, "name":"carrots", "amount:": 0},
    {"id": 3, "name":"milk", "amount:": 1}
]
# Keep track of ID as need to increment for new food in basket
cartId = 4

##################################################################
# getAll()
#
# Action = Get all foods from DB
# curl "http://127.0.0.1:5000/foods"

@app.route('/foods')
def getAll():
    #return "in getAll"

    # Connect to food table in datarepresentation DB!
    results = foodDAO.getAll()
    return jsonify(results)
    #return results

##################################################################
# findByID(id)
#
# Action = Find food in DB by ID
# curl "http://127.0.0.1:5000/foods/1"

@app.route('/foods/<int:id>')
def findByID(id):
    #return "in find by ID for id "+ str(id)

    # Return food from DB by requested id
    foundFood = foodDAO.findByID(id)

    # Check if id exists
    if not foundFood:
        return "That id does not exist in the database table"
        abort(404)
    
    return jsonify(foundFood)

##################################################################
# create()
#
# Action = Create a new food in the DB
# curl -i -H "Content-Type:application/json" -X POST -d "{\"Category\": \"vegetable\", \"Name\":\"onion\", \"Price\": 0.50 }" "http://127.0.0.1:5000/foods"

@app.route('/foods', methods=['POST'])
def create():
    #return "in create"

    if not request.json:
        abort(400)
    # Do other checking for more marks eg proper format? price a decimal

    # id increments automatically - watch order of attributes. 
    food = {
        "Category": request.json['Category'],
        "Name": request.json['Name'],
        "Price": request.json['Price'] 
    }

    # Make the tuple for DB
    values = (food['Category'], food['Name'], food['Price'])
    newId = foodDAO.create(values)
    food['id'] = newId

    return jsonify(food)

##################################################################
# update(id)
#
# Action = Update food in DB by ID
# curl -i -H "Content-Type:application/json" -X PUT -d "{\"Price\":44.44}" "http://127.0.0.1:5000/foods/3"

@app.route('/foods/<int:id>', methods=['PUT'])
def update(id):
    #return "in update by ID for id "+ str(id)

    # Find the food in DB table
    foundFood = foodDAO.findByID(id)

    if not foundFood:
        return "That id does not exist in the database table"
        abort(404)

    if not request.json:
        abort(400)

    # Get what was passed up
    reqJson = request.json

    # Error checking - price a decimal - do later
    #if ('Price' in reqJson and type(reqJson['Price']) is not int):
    #    abort(400)

    # Info to update    
    if 'Category' in reqJson:
        foundFood['Category'] = reqJson['Category']
    if 'Name' in reqJson: 
        foundFood['Name'] = reqJson['Name']
    if 'Price' in reqJson:
        foundFood['Price'] = reqJson['Price']

    # Make the tuple for DB
    values = (foundFood['Category'], foundFood['Name'], foundFood['Price'], foundFood['id'])
    # Do the update on DB
    foodDAO.update(values)
    return jsonify(foundFood)

##################################################################

# Action = Delete food in DB by ID
# curl -X DELETE "http://127.0.0.1:5000/foods/1"

@app.route('/foods/<int:id>', methods=['DELETE'])
def delete(id):
    #return "in delete by ID for id "+ str(id)

    # Check if id exists in food table in DB
    foundFood = foodDAO.findByID(id)
    if not foundFood:
        return "That id does not exist in the database table"
        abort(404)

    # Remove food from DB by id
    foodDAO.delete(id)
    return jsonify({"done":True})

##################################################################

if __name__ == '__main__' :
    app.run(debug= True)