# fleet-maintenance-system

A Django REST Framework API for managing vehicle maintenance tasks.

## Features

- Manage vehicles (create, read, update, delete)
- Create and track maintenance tasks
- Filter maintenance tasks by vehicle registration
- RESTful API endpoints with proper validation and error handling

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/maintenance_system.git
cd maintenance_system
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up the database
```bash
python manage.py migrate
```

5. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### Running the API

Start the development server:
```bash
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/

## API Documentation

### Vehicles

#### List All Vehicles
```
GET /vehicles/
```

Response:
```json
[
  {
    "id": 1,
    "registration_number": "ABC123",
    "make": "Toyota",
    "model": "Corolla",
    "year": 2020
  },
  {
    "id": 2,
    "registration_number": "XYZ789",
    "make": "Honda",
    "model": "Civic",
    "year": 2019
  }
]
```

#### Get Vehicle Details
```
GET /vehicles/{id}/
```

Response:
```json
{
  "id": 1,
  "registration_number": "ABC123",
  "make": "Toyota",
  "model": "Corolla",
  "year": 2020
}
```

#### Create Vehicle
```
POST /vehicles/
```

Request:
```json
{
  "registration_number": "DEF456",
  "make": "Ford",
  "model": "Focus",
  "year": 2021
}
```

#### Update Vehicle
```
PUT /vehicles/{id}/
```

Request:
```json
{
  "registration_number": "DEF456",
  "make": "Ford",
  "model": "Focus ST",
  "year": 2021
}
```

#### Partially Update Vehicle
```
PATCH /vehicles/{id}/
```

Request:
```json
{
  "model": "Focus RS"
}
```

#### Delete Vehicle
```
DELETE /vehicles/{id}/
```

### Maintenance Tasks

#### List All Tasks
```
GET /tasks/
```

Response:
```json
[
  {
    "id": 1,
    "vehicle": 1,
    "task_type": "Oil Change",
    "description": "Regular oil change with filter replacement",
    "status": "completed",
    "created_at": "2025-03-01T10:30:00Z",
    "updated_at": "2025-03-01T14:15:00Z"
  },
  {
    "id": 2,
    "vehicle": 2,
    "task_type": "Brake Inspection",
    "description": "Check brake pads and rotors",
    "status": "pending",
    "created_at": "2025-03-02T09:00:00Z",
    "updated_at": "2025-03-02T09:00:00Z"
  }
]
```

#### Filter Tasks

You can filter tasks by:
- Vehicle registration number: `?registration_number=ABC123`
- Task type: `?task_type=Oil%20Change`
- Status: `?status=completed`

Example:
```
GET /tasks/?registration_number=ABC123&status=completed
```

#### Get Task Details
```
GET /tasks/{id}/
```

Response:
```json
{
  "id": 1,
  "vehicle": 1,
  "task_type": "Oil Change",
  "description": "Regular oil change with filter replacement",
  "status": "completed",
  "created_at": "2025-03-01T10:30:00Z",
  "updated_at": "2025-03-01T14:15:00Z"
}
```

#### Create Task
```
POST /tasks/
```

Request:
```json
{
  "vehicle": 1,
  "task_type": "Tire Rotation",
  "description": "Rotate tires to ensure even wear",
  "status": "pending"
}
```

#### Update Task
```
POST /tasks/{id}/
```

Request:
```json
{
  "vehicle": 1,
  "task_type": "Tire Rotation",
  "description": "Rotate tires to ensure even wear",
  "status": "completed"
}
```

#### Partially Update Task
```
PATCH /tasks/{id}/
```

Request:
```json
{
  "status": "completed"
}
```

#### Delete Task
```
DELETE /tasks/{id}/
```

## Error Handling

The API returns appropriate HTTP status codes:

- 200: Successful operation
- 201: Resource successfully created
- 204: Resource successfully deleted
- 400: Bad request (validation errors)
- 404: Resource not found
- 500: Server error

Example error response:
```json
{
  "error": "Maintenance task not found"
}
```

## Filtering

The API supports filtering maintenance tasks by:
- Vehicle registration number

Example:
```
GET /tasks/?registration_number=ABC123&status=pending
```
