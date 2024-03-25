from fastapi import FastAPI,Request
from api.endpoints import login,items,cart
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException  


app = FastAPI(debug=True)


# Default route for assignment
@app.get("/")
async def default_route():
    return JSONResponse(status_code=200,content={"message": "Welcome to Merge Shopping Cart Assignment"})

app.include_router(login.router, prefix="/api")
app.include_router(items.router, prefix="/api")
app.include_router(cart.router, prefix="/api")


# Define a catch-all route as the last route
@app.route("/{full_path:path}")
async def catch_all(full_path: str):
    return JSONResponse(status_code=404,content={"message": "Please provide valid URL"})


# Custom exception handler for RequestValidationError (validation errors)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        field = error["loc"][-1]
        msg = f"{field} is required"
        error_messages.append({"message": msg})    
    return JSONResponse(status_code=422, content={"status": False, "errors": error_messages})


# Custom exception handler for authentication errors (HTTPException)
@app.exception_handler(StarletteHTTPException)
async def authentication_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"status": False, "errors": [{"message": exc.detail}]})

 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)