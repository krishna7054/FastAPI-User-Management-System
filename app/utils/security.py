from bson import ObjectId
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from app.models import UserInDB

SECRET_KEY = "your-secret-key"  # Secret key used for encoding and decoding JWT tokens
ALGORITHM = "HS256"  # Algorithm used for encoding the JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Context for hashing passwords
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Security scheme for OAuth2 password bearer tokens

client = MongoClient("mongodb+srv://21it3038:WDHbRTNejWX1uisv@cluster0.b8vudo6.mongodb.net/")  # MongoDB client setup
db = client["fastapi_db"]  # Select the 'fastapi_db' database
users_collection = db["users"]  # Select the 'users' collection


# Hash the password using the bcrypt scheme
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)   



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()  # Copy the data dictionary
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Calculate the expiration time
    to_encode.update({"exp": expire})  
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,  # Unauthorized status code
        detail="Could not validate credentials",  # Error detail message
        headers={"WWW-Authenticate": "Bearer"},  # Headers indicating that authentication is required
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the JWT token
        user_id: str = payload.get("sub")  # Extract the user ID from the token payload
        if user_id is None:
            raise credentials_exception  # Raise an error if the user ID is missing
        user = users_collection.find_one({"_id": ObjectId(user_id)})  # Find the user in the database by ID
        if user is None:
            raise credentials_exception  # Raise an error if the user is not found
        return user  # Return the user document
    except JWTError:
        raise credentials_exception  # Raise an error if JWT decoding fails