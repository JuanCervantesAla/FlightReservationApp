from database.mongo import flights_collection
from bson.objectid import ObjectId

async def get_flights():
    flights = await flights_collection.find().to_list(100)
    return [serialize_flight(flight) for flight in flights]

def serialize_flight(flight):
    flight["id"] = str(flight["_id"])
    del flight["_id"]
    return flight

async def reserve_space(flight_id):
    flight = await flights_collection.find_one({"_id": ObjectId(flight_id)})
    if flight and flight["sits"] > 0:
        result = await flights_collection.update_one(
            {"_id": ObjectId(flight_id), "sits": {"$gt": 0}},
            {"$inc": {"sits": -1}}
        )

        return result.modified_count > 0
    return False