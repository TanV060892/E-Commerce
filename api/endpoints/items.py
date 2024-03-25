from fastapi import Depends,APIRouter,Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from common import User,get_current_user
from database import get_query_result,execute_insertion_query


# Model for items request
class Item(BaseModel):
    name: str
    quantity: int
    price: float

#api call starts from here
router = APIRouter()

# API to add new items
@router.post("/items")
async def add_items(item: Item, current_user: User = Depends(get_current_user)):
    if current_user.role == "admin":
        item = item.dict()
        query = "INSERT INTO items (name, quantity, price) VALUES (:name, :quantity, :price)"
        params = { 'name': item['name'], 'quantity': item['quantity'], 'price': item['price'] }
        result = await execute_insertion_query(query, params)
        if 'response' in result : 
            return JSONResponse(status_code=201, content={"status": True, "message": "Item added successfully."})
        else : 
            return JSONResponse(status_code=500, content={"status": False, "error": "Sorry! Unable to get details due to technical issue."})
    else:
        return JSONResponse(status_code=403, content={"status": False, "error": "Permission denied"})


# API to view all added items
@router.get("/items")
async def view_items(current_user: User = Depends(get_current_user)):
    if current_user.role == "user":
        result = await get_query_result("SELECT id,name,quantity,price,TO_CHAR(TO_TIMESTAMP(added_on), 'DD-MM-YYYY HH24:MI:SS')added_on FROM items")
        if 'response' in result :
            return JSONResponse(status_code=200, content={"status": True, "items": result['response']})
        else : 
            return JSONResponse(status_code=500, content={"status": False, "error": "Sorry! Unable to get details due to technical issue."})
    else:
        return JSONResponse(status_code=403, content={"status": False, "error": "Permission denied"})
    
    
