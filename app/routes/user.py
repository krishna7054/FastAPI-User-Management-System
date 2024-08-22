from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.models import UserInDB
from app.utils.security import get_current_user
from pymongo import MongoClient

# Create an instance of APIRouter to define our API endpoints
router = APIRouter()

# Set up the MongoDB client and connect to the database
client = MongoClient("mongodb+srv://21it3038:WDHbRTNejWX1uisv@cluster0.b8vudo6.mongodb.net/")
db = client["fastapi_db"]  # Select the 'fastapi_db' database
users_collection = db["users"]  # Select the 'users' collection


#  Linking ID API
@router.put("/{user_id}/link_id/")
async def link_id(user_id: str, external_id: str):
    # Find the user by their ID
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    
    # If the user does not exist, raise a 404 error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user document with the provided external_id
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"external_id": external_id}}
    )
    
    # If no documents were modified, raise a 400 error
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to link ID")
    
    # Return a success message with the user_id and external_id
    return {"message": "ID linked successfully", "user_id": user_id, "external_id": external_id}


# Joins API
@router.get("/{user_id}/full_profile/")
async def get_user_with_linked_data(user_id: str):
    try:
        # Define the aggregation pipeline for querying the user with linked data
        pipeline = [
            {"$match": {"_id": ObjectId(user_id)}},
            {
                "$lookup": {
                    "from": "linked_collection",  # Replace with the actual collection name
                    "localField": "external_id",
                    "foreignField": "_id",
                    "as": "linked_data"
                }
            }
        ]
        # Perform aggregation query on the 'users' collection
        user = list(users_collection.aggregate(pipeline))
        
        # If no user is found, raise a 404 error
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert ObjectId fields to strings for JSON serialization
        def convert_objectid(obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            if isinstance(obj, dict):
                return {k: convert_objectid(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert_objectid(i) for i in obj]
            return obj

        # Convert the ObjectId fields in the user document
        user = convert_objectid(user[0])
        
        # Return the user document with linked data
        return user

    except Exception as e:
        # Print the exception details and raise a 500 error
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Chain Delete API
@router.delete("/{user_id}/")
async def delete_user_and_associated_data(user_id: str):
    # Find the user by their ID
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    
    # If the user does not exist, raise a 404 error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete associated data in other collections
    db.linked_collection.delete_many({"user_id": ObjectId(user_id)})  # Replace with actual collection name
    
    # Delete the user from the 'users' collection
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    
    # If no documents were deleted, raise a 400 error
    if result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="Failed to delete user")
    
    # Return a success message indicating that the user and associated data were deleted
    return {"message": "User and associated data deleted successfully"}
