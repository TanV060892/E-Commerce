from fastapi import Depends,APIRouter,Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from common import USERS_DETAILS,User,get_current_user

# Model for login request
class LoginRequest(BaseModel):
    username: str 
    password: str 

# Model for user suspension request
class USuspension(BaseModel):
    username: str 
   
    
#api call starts from here
router = APIRouter()

@router.post("/token")
def login(request: Request, request_data: LoginRequest):
    user = USERS_DETAILS.get(request_data.username)
    if user is None or request_data.password != user["password"]:
        return JSONResponse(status_code=401, content={"status": False, "error": "Invalid Credentials."}) 
    return JSONResponse(status_code=200, content={"status": True, "access_token": request_data.username, "token_type": "bearer"})


# Restricted API endpoint for admin
@router.get("/admin")
def admin_resource(request: Request,current_user: User = Depends(get_current_user)):
    if current_user.role == "admin" :
        return JSONResponse(status_code=200, content={"status": True, "message": "Permission granted.","role":"admin","services":USERS_DETAILS.get(current_user.role)['services']})
    else :
        return JSONResponse(status_code=403, content={"status": False, "error": "Permission denied."}) 
    

# Restricted API endpoint for user
@router.get("/user")
def user_resource(request: Request,current_user: User = Depends(get_current_user)):
    if current_user.role == "user" :
        return JSONResponse(status_code=200, content={"status": True, "message": "Permission granted.","role":"admin","services":USERS_DETAILS.get(current_user.role)['services']})
    else :
        return JSONResponse(status_code=403, content={"status": False, "error": "Permission denied."}) 
    

# API endpoint to suspend user
@router.put("/user/suspend")
def user_resource(user: USuspension,current_user: User = Depends(get_current_user)):
    if current_user.role == "admin" :        
        # Check if the user to suspend exists in your user data
        user_to_suspend = USERS_DETAILS.get(user.username)
        if user_to_suspend:
            # Implement suspension logic here (e.g., set user status to suspended)
            # Return a detailed response with suspension information
            return JSONResponse( status_code=200, content={ "status": True, "message": f"User '{user.username}' has been suspended." } )
        else:
            return JSONResponse( status_code=404, content={ "status": False, "error": f"User '{user.username}' not found." } )
        
    else :
        return JSONResponse(status_code=403, content={"status": False, "error": "Permission denied."}) 



