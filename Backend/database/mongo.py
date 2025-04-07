from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://superemiliano:1234@localhost:27017/reservation_system?authSource=admin"
client = AsyncIOMotorClient(MONGO_URL)
db = client["reservation_system"]

flights_collection = db["flights"]
reservations_collection = db["reservations"]
users_collection = db["users"]