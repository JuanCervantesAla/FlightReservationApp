from database.mongo import flights_collection
from bson.objectid import ObjectId

#File to get some data from the flights direct from mongodb

#Get all the flights
async def get_flights():
    flights = await flights_collection.find().to_list(100)
    return [serialize_flight(flight) for flight in flights]

#Serialize the data from mongo to fastapi undestandable
def serialize_flight(flight):
    flight["id"] = str(flight["_id"])
    del flight["_id"]
    return flight

#Makes a reservation on the flight, gets the flight and remove -1 from available sits
#Return false or the modified count
async def reserve_space(flight_id):
    flight = await flights_collection.find_one({"_id": ObjectId(flight_id)})
    if flight and flight["sits"] > 0:
        result = await flights_collection.update_one(
            {"_id": ObjectId(flight_id), "sits": {"$gt": 0}},
            {"$inc": {"sits": -1}}
        )

        return result.modified_count > 0
    return False