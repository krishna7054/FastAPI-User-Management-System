# FastAPI User Management System

## Overview

This project is a FastAPI-based user management system that supports user registration, login, linking external IDs, fetching user profiles with linked data, and deleting users along with their associated data. It utilizes MongoDB for data storage and includes JWT-based authentication.

## Features

1. **User Registration**: Allows new users to register with a username, email, and password.
2. **User Login**: Authenticates users using email and password, and provides a JWT for secure access.
3. **Link External ID**: Enables users to link an external ID to their account.
4. **Fetch User Profile**: Retrieves a user's profile along with data from a linked collection.
5. **Delete User**: Deletes a user and their associated data from the database.

## Installation

### Prerequisites

- Python 3.7 or higher
- MongoDB instance (Atlas or local)
- `pip` for installing Python packages

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/krishna7054/FastAPI-User-Management-System.git
   cd FastAPI-User-Management-System
    ```
2. **Create a virtual environment**:

   ```bash
    python -m venv venv
   ```
3. **Activate the virtual environment**:
  - ***On Windows***:
  ```bash
  venv\Scripts\activate
```
  - ***On macOS/Linux***:
  ```bash
  source venv/bin/activate
```
4. **Install dependencies**:
  ```bash
  pip install -r requirements.txt
```
5. **Configure MongoDB**:
  Update the MongoDB URI in app/utils/security.py with your MongoDB connection string.

6. **Run the application**:
  ```bash
  uvicorn main:app --reload
```
The application will be available at `http://127.0.0.1:8000`.

# API Endpoints
## User Registration
- Endpoint: /auth/register
- Method: POST
- Request Body:
```bash
{
  "username": "exampleuser",
  "email": "user@example.com",
  "password": "password123"
}
```
- Response:
```bash
{
  "id": "unique_user_id"
}
```
- Preview:![p1](https://github.com/user-attachments/assets/241bb9e2-2cdf-4bfd-862f-c1e1d3a45e87)

## User Login
- Endpoint: /auth/login
- Method: POST
- Request Body:
```bash
{
  "email": "user@example.com",
  "password": "password123"
}
```
- Response:
```bash
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```
-  Preview:![p2](https://github.com/user-attachments/assets/7bd54a3e-3d33-45ad-892e-2224b0579cb4)

## Link External ID
- Endpoint: /users/{user_id}/link_id/
- Method: PUT
- Request Body:
```bash
{
  "external_id": "external_id_value"
}
```
- Response:
```bash
{
  "message": "ID linked successfully",
  "user_id": "user_id",
  "external_id": "external_id_value"
}
```
- Preview:![p3](https://github.com/user-attachments/assets/c57824c3-8266-4f8d-9747-a9c2450d585e)

## Fetch User Profile with Linked Data
- Endpoint: /users/{user_id}/full_profile/
- Method: GET
- Response:
```bash
{
  "id": "user_id",
  "username": "exampleuser",
  "email": "user@example.com",
  "hashed_password": "hashed_password_value",
  "linked_data": [
    {
      "field1": "value1",
      "field2": "value2"
    }
  ]
}
```
- Preview:![p4](https://github.com/user-attachments/assets/e38cd1ae-e6c7-4bab-8a49-3271bf2b78be)

## Delete User and Associated Data
- Endpoint: /users/{user_id}/
- Method: DELETE
- Response:
```bash
{
  "message": "User and associated data deleted successfully"
}
```

- Preview:![p5](https://github.com/user-attachments/assets/b5727584-297a-4feb-a00a-1c66f6cff43d)
