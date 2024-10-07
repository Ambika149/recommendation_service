# Job Recommendation Service

This is a FastAPI-based web application that provides job recommendations based on a user's profile. The application queries a database of job postings and matches them with the user's skills, experience level, and preferences.

## Features

- Accepts user profile data via an API request.
- Matches job postings based on experience level, skills, locations, and job type.
- Returns a list of recommended jobs.
- Provides structured error handling and logging for easy debugging.

## Table of Contents

- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Testing](#testing)

## Installation

1. Clone the repository:

    ```bash
    git clone <repo_url>
    cd <project>
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv env
    source env/bin/activate  # For Linux/macOS
    # OR
    .\env\Scripts\activate  # For Windows
    ```

3. Install the required dependencies:

    ```bash
   poetry install
    ```

## Environment Setup

1. Ensure you have the following environment variables configured (if needed for your database):

    ```bash
    export DATABASE_URL=postgresql://user:password@localhost:5432/job_db
    ```

2. Update your database URL in the FastAPI app or in the `app.db.model` for the SQLAlchemy connection.

## Database Setup

1. Create the necessary tables in your database:

    ```bash
    alembic upgrade head  # If using Alembic for migrations
    ```

2. Make sure the job postings table (`job_postings`) is populated with relevant job data.

## Running the Application

To run the FastAPI app:

```bash
uvicorn main:app --reload


API Endpoints
POST /recommendations

Accepts user profile data and returns job recommendations based on the input.

    Request Body: The following example shows the required structure:
{
    "name": "John Doe",
    "skills": ["Python", "FastAPI", "SQL"],
    "experience_level": "Intermediate",
    "preferences": {
        "desired_roles": ["Backend Developer", "Software Engineer"],
        "locations": ["San Francisco", "Remote"],
        "job_type": "Full-Time"
    }
}


Response: A list of job postings matching the user's profile. Example:
[
    {
        "job_title": "Software Engineer",
        "company": "Tech Solutions Inc.",
        "location": "San Francisco",
        "job_type": "Full-Time",
        "required_skills": ["JavaScript", "React", "Node.js"],
        "experience_level": "Intermediate"
    }
]

