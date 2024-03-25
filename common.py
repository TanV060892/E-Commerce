from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional,Dict

# Model for user response
class User(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    error: Optional[str] = None

# Sample user data (for demonstration purposes; use a database in production)
USERS_DETAILS = {
    "admin": {"username": "admin", "password": "adminpassword", "role": "admin","services":["Add items","Suspend user"]},
    "user": {"username": "user", "password": "userpassword", "role": "user","services":["List available items","Add items to a cart","Remove items from their cart"]},
}

# OAuth2 password flow for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper function to get the current user based on the access token
def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = USERS_DETAILS.get(token)    
    if user_data is None:
        user_data = {"error": "Invalid Token"}
    return User(**user_data)