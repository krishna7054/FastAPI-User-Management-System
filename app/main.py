from fastapi import FastAPI
from app.routes import auth, user

# Create an instance of the FastAPI application
app = FastAPI()

# Include the router for authentication-related routes
# - `auth.router` is the router instance from the `auth` module
# - `prefix="/auth"` adds the `/auth` prefix to all routes in this router
# - `tags=["auth"]` groups these routes under the "auth" tag in the API documentation
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include the router for user-related routes
# - `user.router` is the router instance from the `user` module
# - `prefix="/users"` adds the `/users` prefix to all routes in this router
# - `tags=["users"]` groups these routes under the "users" tag in the API documentation
app.include_router(user.router, prefix="/users", tags=["users"])
