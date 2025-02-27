# User Management CRUD API

This is a Python-based RESTful API for managing users, built using Flask and SQLAlchemy.

## Features

- Create, Read, Update, and Delete (CRUD) operations for users.
- Modular structure with clear separation of concerns.
- Proper error handling with HTTP status codes.
- Unit tests to ensure functionality.

---

## How to Run the Code

Follow these steps to set up and run the application:

### 1. Set Up the Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Start the Flask server:

```bash
python app.py
```

The server will run at `http://127.0.0.1:5000`.

### 4. Run the Unit Tests

Execute the unit tests to verify functionality:

```bash
python -m unittest discover tests
```

---

## Example API Endpoints

### Create a User
- **POST** `/api/users`
- Request Body:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```

### Get All Users
- **GET** `/api/users`

### Get a User by ID
- **GET** `/api/users/<id>`

### Update a User
- **PUT** `/api/users/<id>`
- Request Body:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com"
  }
  ```

### Delete a User
- **DELETE** `/api/users/<id>`

---

## Output Example

After running the application, here’s what the responses might look like:

- **GET /api/users**:
  ```json
  []
  ```

- **POST /api/users**:
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```
