from fastapi import Depends,APIRouter,Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from common import USERS_DETAILS,User,get_current_user
from database import get_query_result,execute_query_block


# Model for items request
class CItem(BaseModel):
    code: int
    quantity: int

#api call starts from here
router = APIRouter()

# API to add new items to cart
@router.post("/cart")
async def add_items_to_cart(citem: CItem, current_user: User = Depends(get_current_user)):
    if current_user.role == "user":
        item_code = citem.code
        item_quantity = citem.quantity
        
        # Check if the item exists in stock
        item_in_stock = None
        ITEMS = []
        result = await get_query_result("SELECT id code,name,quantity,price FROM items where id = "+str(item_code)+"")
        if 'response' in result and len(result['response']) > 0:
            ITEMS = result['response']

        for item in ITEMS:
            if item["code"] == item_code:
                item_in_stock = item
                break

        if item_in_stock and item_in_stock["quantity"] >= item_quantity:
            # Remove the requested quantity from stock
            item_in_stock["quantity"] -= item_quantity
            query = "DO $$ DECLARE row_count INT; BEGIN UPDATE items SET quantity = "+str(item_in_stock["quantity"])+" WHERE ID = "+str(item["code"])+"; UPDATE cart SET quantity = "+str(item_quantity)+", price = "+str(item_in_stock["price"])+" WHERE item_id = "+str(item["code"])+" RETURNING 1 INTO row_count; IF row_count is null THEN INSERT INTO cart (user_id, quantity, price, item_id) VALUES ('user',"+str(item_quantity)+", "+str(item_in_stock["price"])+", "+str(item_code)+"); END IF; END $$;"
            result = await execute_query_block(query)
            if 'response' in result : 
                return JSONResponse( status_code=201, content={"status": True, "message": f"Item '{item_code}' added to cart successfully."} )
            else : 
                return JSONResponse(status_code=500, content={"status": False, "error": "Sorry! Unable to add details due to technical issue."})           
        else:
            return JSONResponse( status_code=400, content={"status": False, "error": "Item not available in stock or insufficient quantity."} )
    else:
        return JSONResponse(status_code=403, content={"status": False, "error": "Permission denied."})
    

# API to remove items from the cart
@router.delete("/cart/{item_code}")
async def remove_item_from_cart(item_code: int, current_user: User = Depends(get_current_user)):
    if current_user.role == "user":
        # Check if the item exists in the cart
        item_to_remove = None
        ITEMS = CART_ITEMS = []
        result = await get_query_result("SELECT id code,name,quantity,price FROM items")
        if 'response' in result and len(result['response']) > 0:
            ITEMS = result['response']

        result = await get_query_result("SELECT quantity,price,item_id code FROM cart where item_id = "+str(item_code)+"")
        
        if 'response' in result and len(result['response']) > 0:
            CART_ITEMS = result['response']
        for item in CART_ITEMS:
            if item["code"] == item_code:
                item_to_remove = item
                break
        
        if item_to_remove:
            # Update the stock with the removed quantity
            for stock_item in ITEMS:
                if stock_item["code"] == item_code:
                    stock_item["quantity"] += item_to_remove["quantity"]
                    break
            
            # Remove the item from the cart
            query = "DO $$ DECLARE row_count INT; BEGIN UPDATE items SET quantity = "+str(stock_item["quantity"])+" WHERE ID = "+str(item_code)+"; DELETE FROM CART WHERE ITEM_ID = "+str(item_code)+";  END $$;"
            result = await execute_query_block(query)
            if 'response' in result : 
                return JSONResponse( status_code=200, content={"status": True, "message": f"Item '{item_code}' removed from the cart."} )
            else : 
                return JSONResponse(status_code=500, content={"status": False, "error": "Sorry! Unable to delete details due to technical issue."})    
                       
        else:
            return JSONResponse( status_code=400, content={"status": False, "error": f"Item '{item_code}' not found in the cart."} )
    else:
        return JSONResponse(status_code=403, content={"status": False, "error": "Permission denied."})

#Add coupons details
@router.post("/coupon")
async def add_items_to_cart(citem: CItem, current_user: User = Depends(get_current_user)):
    if current_user.role == "admin":
        item_code = citem.code
        item_quantity = citem.quantity
        
        # Check if the item exists in stock
        item_in_stock = None
        ITEMS = []
        result = await get_query_result("SELECT id code,name,quantity,price FROM items where id = "+str(item_code)+"")
        if 'response' in result and len(result['response']) > 0:
            ITEMS = result['response']

        for item in ITEMS:
            if item["code"] == item_code:
                item_in_stock = item
                break
            item_in_stock["quantity"] -= item_quantity
            query = "DO $$ DECLARE row_count INT; BEGIN UPDATE items SET quantity = "+str(item_in_stock["quantity"])+" WHERE ID = "+str(item["code"])+"; UPDATE cart SET quantity = "+str(item_quantity)+", price = "+str(item_in_stock["price"])+" WHERE item_id = "+str(item["code"])+" RETURNING 1 INTO row_count; IF row_count is null THEN INSERT INTO cart (user_id, quantity, price, item_id) VALUES ('user',"+str(item_quantity)+", "+str(item_in_stock["price"])+", "+str(item_code)+"); END IF; END $$;"
            result = await execute_query_block(query)
            if 'response' in result : 
                return JSONResponse( status_code=201, content={"status": True, "message": f"Item '{item_code}' added to cart successfully."} )
            else : 
                return JSONResponse(status_code=500, content={"status": False, "error": "Sorry! Unable to add details due to technical issue."})           
    else:
        return JSONResponse(status_code=403, content={"status": False, "error": "Permission denied."})