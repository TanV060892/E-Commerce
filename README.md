# Pre-requisites

- Install [Python] version 3.10.0

# Getting started

- Clone the repository

```
git clone https://github.com/Credain/Bank_Integration.git
```

- Install dependencies

```
pip install -r requirements.txt
```

- Build and run the project

```
On Windows :
python -m venv venv
.\venv\Scripts\activate
uvicorn main:app --reload
```


- Health Check

  Endpoint : http://localhost:8000/

## Endpoints

  The application provides the following API endpoints:
  
  POST /api/token: User login endpoint to obtain an access token.
  
  GET /api/admin: Restricted endpoint for admin to see available services can use.
  
  GET /api/user: Restricted endpoint for regular users to see available services can use.

  PUT /api/user/suspend: Restricted endpoint for admin to suspend user.

  GET /api/items: User endpoint to view all available items.

  POST /api/items: User endpoint to add new items.

  POST /api/cart: User endpoint to add new item to cart from available listed items from stock.

  DELETE /api/cart/{item_code}: User endpoint to remove item from cart.

  POST /api/coupon: Add new coupons.

  GET /api/discount: Checks valid coupons applied and get discounted amount of cart value

## Authentication
  
  This application uses OAuth2 password flow for authentication. To obtain an access token, make a POST request to /api/token with valid credentials.

  Example:

  ```http
    POST /api/token
    Content-Type: application/json
    
    {
      "username": "admin",
      "password": "adminpassword"
    }
  ```
  The response will include an access token that you can use to access the restricted endpoints.

## Database
  
  This application uses Postgresql Database. After successful installation perform below queries to create tables to test

  Queries:

  ```
   CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    quantity INT,
    price FLOAT,
    added_on DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)
);

CREATE TABLE cart (
    user_id VARCHAR(20),
    quantity INT,
    price FLOAT,
    item_id INT,
    FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE coupon (
    code VARCHAR(20),
    valid_till INT,
    description VARCHAR(200),
    discount_percentage INT
);
  ```
  
## Sample User Data

  For demonstration purposes, the application uses sample user data stored in-memory. In a production environment, replace this with a database or a more secure storage mechanism.

  Sample User Data:
  
    Admin User:
    
      Username: admin
      
      Password: adminpassword
      
      Role: admin
      
      Services: ["Add items", "Suspend user"]
    
    Regular User:
    
      Username: user
      
      Password: userpassword
      
      Role: user
      
      Services: ["List available items", "Add items to a cart", "Remove items from their cart"]


## Running Tests

  This project includes end-to-end (E2E) tests to ensure the functionality of the application. To run the tests, use the following command:

  ```bash
     pytest tests/cart_e2e.py
     pytest tests/items_e2e.py
     pytest tests/login_e2e.py
  ```
  Make sure to install pytest and httpx if you haven't already:

  ```bashbash
    pip install pytest httpx
  ```

## Contributing

  If you'd like to contribute to this project, please follow the standard GitHub fork and pull request workflow.

## License

  This project is licensed under the MIT License.

  Please customize the placeholder values (e.g., URLs, usernames, and passwords) and other information to match your specific project details. You can also format and style the `README.md` file further to meet your preferences.
  
