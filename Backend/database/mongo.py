from motor.motor_asyncio import AsyncIOMotorClient

#This class makes a conn with the database and gets the collections of it

MONGO_URL = "mongodb://superemiliano:1234@localhost:27017/reservation_system?authSource=admin"
client = AsyncIOMotorClient(MONGO_URL)
db = client["reservation_system"]

#Get the collections
flights_collection = db["flights"]
reservations_collection = db["reservations"]
users_collection = db["users"]