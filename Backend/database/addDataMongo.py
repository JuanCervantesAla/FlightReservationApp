from pymongo import MongoClient
from bson import ObjectId

# This class is just to hardcore data into the database, example data as flights and users
# Makes a connection
#  Insert on mongodb database
#

client = MongoClient("mongodb://superemiliano:1234@localhost:27017/reservation_system?authSource=admin")
db = client["reservation_system"]

#Hardcore all the flighst with false data
def addFlights():
    db.flights.insert_many([
        {"from": "Guadalajara", "to": "Madrid", "sits": 20, "price":2345,"date":"14/5/25"},
        {"from": "Monterrey", "to": "Toronto", "sits": 15, "price":4566,"date":"23/9/25"},
        {"from": "CDMX", "to": "Dallas", "sits": 15, "price":4566,"date":"14/20/22"},
        {"from": "Oaxaca", "to": "Turquia", "sits": 15, "price":4566,"date":"09/12/35"},
        {"from": "Apodaca", "to": "Marruecos", "sits": 15, "price":4566,"date":"13/8/28"},
        {"from": "China", "to": "Japon", "sits": 15, "price":4566,"date":"30/2/25"},
        {"from": "Ucrania", "to": "Rusia", "sits": 15, "price":4566,"date":"24/6/25"},
    ])

#Hardcode the users
def addUsers():
    db.users.insert_many([
        {"name": "Juan", "email":"Juan@gmail.com", "password":"12345"},
        {"name": "Jose", "email":"Jose@gmail.com", "password":"12345"},
        {"name": "Emiliano", "email":"Emiliano@gmail.com", "password":"12345"},
        {"name": "Pedro", "email":"Pedro@gmail.com", "password":"12345"},
        {"name": "Pancho", "email":"Pancho@gmail.com", "password":"12345"},
        {"name": "Sabrina Carpenter", "email":"Sabrina@gmail.com", "password":"12345"},
        {"name": "Elton John", "email":"Elton@gmail.com", "password":"12345"},
    ])