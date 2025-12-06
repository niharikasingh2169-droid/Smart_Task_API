# Task Dashboard API

Enterprise-level FastAPI application for task management with layered architecture.

## Project Structure

```
Task_dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py      # SQLite database connection and initialization
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py            # Pydantic models for request/response
│   ├── repository/
│   │   ├── __init__.py
│   │   └── task_repository.py # Data access layer
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py    # Business logic layer
│   │   └── openai_service.py  # OpenAI integration service
│   └── routes/
│       ├── __init__.py
│       └── task_routes.py     # API route handlers
├── requirements.txt
├── .env.example
└── README.md
```

## Architecture

The project follows a clean architecture pattern with three main layers:

1. **Route Layer** (`app/routes/`): Handles HTTP requests and responses
2. **Business Layer** (`app/services/`): Contains business logic and orchestration
3. **Repository Layer** (`app/repository/`): Handles database operations

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key (for priority scoring feature)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following required key-value pairs:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   **Required Environment Variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key for the priority scoring feature. You can obtain this from [OpenAI's website](https://platform.openai.com/api-keys).
   
   **Note:** Make sure the `.env` file is in the project root directory (same level as `requirements.txt`). The `.env` file should not be committed to version control.

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Database

The application uses SQLite with a `Task` table containing:
- `Id` (INTEGER, Primary Key, Auto-increment)
- `Title` (TEXT, Required)
- `Description` (TEXT, Optional)
- `Due_Date` (TEXT, Required)
- `Status` (TEXT, Required)
- `Created_At` (TEXT, Auto-generated timestamp)

The database file `task_dashboard.db` will be created automatically on first run.

## API Endpoints

### 1. Create Task
- **Method**: POST
- **URL**: `/api/tasks/`
- **Body**:
  ```json
  {
    "Title": "Complete project",
    "Description": "Finish the task dashboard project",
    "Due_Date": "2024-12-31",
    "Status": "Pending"
  }
  ```

### 2. Get All Tasks
- **Method**: GET
- **URL**: `/api/tasks/`
- **Response**: List of all tasks

### 3. Get Task by ID
- **Method**: GET
- **URL**: `/api/tasks/{task_id}`
- **Response**: Task details

### 4. Update Task
- **Method**: PUT
- **URL**: `/api/tasks/{task_id}`
- **Body**: (All fields optional)
  ```json
  {
    "Title": "Updated title",
    "Status": "In Progress"
  }
  ```

### 5. Delete Task
- **Method**: DELETE
- **URL**: `/api/tasks/{task_id}`

### 6. Fetch Priority
- **Method**: GET
- **URL**: `/api/tasks/{task_id}/priority`
- **Response**: Priority score (1-5, where 1 is highest priority) with reasoning

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing

You can test the API using the Swagger UI at `/docs` or using tools like curl or Postman.

Example curl commands:

```bash
# Create a task
curl -X POST "http://localhost:8000/api/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"Title": "Test Task", "Description": "Test Description", "Due_Date": "2024-12-31", "Status": "Pending"}'

# Get all tasks
curl -X GET "http://localhost:8000/api/tasks/"

# Get task by ID
curl -X GET "http://localhost:8000/api/tasks/1"

# Update task
curl -X PUT "http://localhost:8000/api/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"Status": "Completed"}'

# Delete task
curl -X DELETE "http://localhost:8000/api/tasks/1"

# Fetch priority
curl -X GET "http://localhost:8000/api/tasks/1/priority"
```
