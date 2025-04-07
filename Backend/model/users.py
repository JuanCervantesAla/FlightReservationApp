from database.mongo import users_collection
from bson.objectid import ObjectId

async def validate_user(user_id):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return user is not None

async def get_users():
    users = await users_collection.find().to_list(100)
    return [serialize_user(user) for user in users]

def serialize_user(user):
    user["id"] = str(user["_id"])
    del user["_id"]
    return user