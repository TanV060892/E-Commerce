from sqlalchemy import create_engine
from databases import Database
import os, asyncpg

# Create a databases.Database instance
database = Database("postgresql://postgres:9699319900vcET&@localhost:5432/postgres") #in realtime application replace with variable value from.env file

# Function to get query results
async def get_query_result(query: str):
    try:
        # Ensure that the database connection is established
        await database.connect()
        async with database.transaction():
            result = await database.fetch_all(query)
            # Convert records to dictionaries
            response_data = [dict(record) for record in result]  
            response_data = [{key: "" if value is None else value for key, value in row.items()} for row in response_data]    
            return {"response": response_data}
    except Exception as e:
        # You can log the error or raise a custom exception here
        return {"error": str(e)}
    finally:
        # Ensure that the database connection is always closed
        await database.disconnect()


# Function to insert query details
async def execute_insertion_query(query: str, *params):
    try:
        # Ensure that the database connection is established
        await database.connect()
        # Execute the insert query with optional parameters
        await database.execute(query, *params)
        return {"response": True}
    except Exception as e:
        # Handle exceptions, log errors, or raise custom exceptions as needed
        return {"error": str(e)}
    finally:
        # Ensure that the database connection is always closed
        await database.disconnect()


# Function to insert query details
async def execute_query_block(query: str):
    try:
        # Ensure that the database connection is established
        await database.connect()
        # Execute the insert query with optional parameters
        await database.execute(query)
        return {"response": True}
    except Exception as e:
        # Handle exceptions, log errors, or raise custom exceptions as needed
        return {"error": str(e)}
    finally:
        # Ensure that the database connection is always closed
        await database.disconnect()








