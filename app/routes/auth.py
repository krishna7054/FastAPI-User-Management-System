from fastapi import APIRouter, HTTPException, Depends
from app.models import UserCreate, UserLogin, UserInDB
from app.utils.security import get_password_hash, verify_password, create_access_token
from pymongo import MongoClient

# Create an instance of APIRouter to define our API endpoints
router = APIRouter()

# Set up the MongoDB client and connect to the database
client = MongoClient("mongodb+srv://21it3038:WDHbRTNejWX1uisv@cluster0.b8vudo6.mongodb.net/")
db = client["fastapi_db"]  # Select the database
users_collection = db["users"]  # Select the 'users' collection

@router.post("/register")
async def register(user: UserCreate):
    # Check if a user with the provided email already exists in the database
    existing_user = users_collection.find_one({"email": user.email})
    
    # If a user with this email already exists, raise a 400 error
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the user's password before storing it
    hashed_password = get_password_hash(user.password)
    
    # Create a new UserInDB object with the hashed password
    new_user = UserInDB(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    # Insert the new user into the 'users' collection and get the result
    result = users_collection.insert_one(new_user.dict())
    
    # Return the ID of the newly created user as a response
    return {"id": str(result.inserted_id)}

@router.post("/login")
async def login(user: UserLogin):
    # Find the user in the database by email
    db_user = users_collection.find_one({"email": user.email})
    
    # If the user doesn't exist or the password is incorrect, raise a 400 error
    if not db_user or not verify_password(user.password, db_user['hashed_password']):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Create an access token for the authenticated user
    access_token = create_access_token(data={"sub": db_user['email']})
    
    # Return the access token and its type as a response
    return {"access_token": access_token, "token_type": "bearer"}
