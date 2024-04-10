# FastAPI Address Book

This is a simple address book application built with FastAPI.

## Overview
This application provides a RESTful API for basic CRUD (Create, Read, Update, Delete) operations on addresses, as well as a means to query addresses within a specified distance from a given location. It's built using FastAPI, a high-performance Python web framework, and leverages SQLite for data storage.


## Installation
1. Clone the repository:
   ```shell
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```shell
   cd address_book
   ```
   
3. Install dependencies:
   ```shell
   pip install -r requirements.txt
   ```
   
## Running the Application
1. Start the API server::
   ```shell
   uvicorn main:app --reload
   ```
2. Access the API at: http://localhost:8000

3. Access the API documentation (Swagger UI) at: http://localhost:8000/docs


## Endpoints
1. POST /addresses/: Create a new address.
2. GET /addresses/{address_id}: Get details of a specific address.
3. GET /addresses/: Get addresses within a specified distance from a given location.
4. PUT /addresses/{address_id}: Update an existing address.
5. DELETE /addresses/{address_id}: Delete an existing address.

