# Task Manager — Full-Stack Web Application

A full-stack task management application built with Python, FastAPI, SQLite, HTML, CSS, and JavaScript. Users can create, view, update, and delete tasks through a responsive web interface.

## Features

- Create and manage tasks through a web interface
- Mark tasks as completed or incomplete
- Delete tasks
- Store task information persistently using SQLite
- RESTful API supporting CRUD operations
- Interactive API documentation with Swagger UI
- Automated API testing using pytest

## Tech Stack

**Backend:** Python, FastAPI, Uvicorn  
**Database:** SQLite  
**Frontend:** HTML, CSS, JavaScript  
**Testing:** pytest, HTTPX  
**Version Control:** Git and GitHub

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/e1m8n-kh8n/task-manager-api.git
cd task-manager-api
```


### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
uvicorn main:app --reload
```

### 5. Open the application

Web interface: http://127.0.0.1:8000/app/

Interactive API documentation: http://127.0.0.1:8000/docs

The SQLite database is initialized automatically when the application starts.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/tasks` | Retrieve all tasks |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update an existing task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Running Tests

Run the automated test suite using:

```bash
pytest -v
```

Tests cover API functionality, including task creation, retrieval, updates, deletion, and error handling.

## Future Improvements

- User authentication and individual accounts
- Task deadlines and priority levels
- Search and filtering capabilities
- Cloud deployment
- Improved frontend accessibility and mobile responsiveness

## Project Overview

This project demonstrates full-stack application development, REST API design, relational database integration, automated testing, and frontend-to-backend communication.