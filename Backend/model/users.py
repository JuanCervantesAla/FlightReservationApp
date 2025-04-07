from database.mongo import users_collection
from bson.objectid import ObjectId

#File to get user related info

#Validates if the user exists on the database
async def validate_user(user_id):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return user is not None

#Get all the users
async def get_users():
    users = await users_collection.find().to_list(100)
    return [serialize_user(user) for user in users]

#Serialize info from mongo to users
def serialize_user(user):
    user["id"] = str(user["_id"])
    del user["_id"]
    return user