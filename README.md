# Online Poll System Backend Documentation

This documentation supports the **Online Poll System Backend** project developed as part of the **ProDev Backend Engineering** program. The system is designed for real-time poll creation, voting, and result computation using scalable APIs.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Goals](#project-goals)
3. [Technologies Used](#technologies-used)
4. [Key Features](#key-features)
5. [Implementation Process](#implementation-process)
6. [API Documentation](#api-documentation)
7. [Setup Instructions](#setup-instructions)
8. [Usage Examples](#usage-examples)
9. [Evaluation Criteria](#evaluation-criteria)

---

## Project Overview

This case study focuses on developing a backend for an online poll system. The backend provides APIs for poll creation, voting, and real-time result computation. The project emphasizes efficient database design and detailed API documentation.

---

## Project Goals

* **API Development**: Build APIs for creating polls, voting, and fetching results.
* **Database Efficiency**: Design schemas optimized for real-time result computation.
* **Documentation**: Provide detailed API documentation using Swagger.

---

## Technologies Used

* **Django**: High-level Python web framework for rapid backend development.
* **PostgreSQL**: Relational database to manage polls and votes.
* **Swagger (drf-yasg)**: For API documentation.

---

## Key Features

### 1. Poll Management

* API to create polls with multiple options.
* Metadata: creation date, expiration.

### 2. Voting System

* API for casting votes.
* Validations to prevent duplicate voting.

### 3. Result Computation

* Real-time calculation of vote counts.
* Optimized queries for scalability.

### 4. API Documentation

* Swagger-based docs hosted at \\.

---

## Implementation Process

### Git Commit Workflow

* **Initial Setup**:

  * feat: set up Django project with PostgreSQL
* **Feature Development**:

  * feat: implement poll creation and voting APIs
  * feat: add results computation API
* **Optimization**:

  * perf: optimize vote counting queries
* **Documentation**:

  * feat: integrate Swagger documentation
  * docs: update README with API usage

---

## API Documentation

Interactive Swagger docs are hosted at:

* http://localhost:8000/api/docs/

Provides detailed descriptions and example requests for:

* POST /api/polls/: Create a poll
* GET /api/polls/: List all polls
* POST /api/vote/: Cast a vote
* GET /api/polls/<id>/results/: View results

---

## Setup Instructions

1. Clone the repository:

   
bash
   git clone <repo_url>
   cd polls-backend


2. Create a virtual environment and activate:

   
bash
   python -m venv env
   source env/bin/activate


3. Install dependencies:

   
bash
   pip install -r requirements.txt


4. Configure .env file and PostgreSQL database.

5. Run migrations:

   
bash
   python manage.py migrate


6. Run development server:

   
bash
   python manage.py runserver


---

## Usage Examples

### Create a Poll

json
POST /api/polls/
{
  "question": "What is your favorite language?",
  "options": ["Python", "JavaScript", "Go"]
}


### Vote on a Poll

json
POST /api/vote/
{
  "poll_id": 1,
  "option_id": 2
}


### Get Poll Results

json
GET /api/polls/1/results/


---

## Evaluation Criteria

### 1. Functionality

* Poll creation, voting, and result computation work flawlessly.

### 2. Code Quality

* Modular and clean code following Django best practices.
* PostgreSQL models are normalized and efficient.

### 3. Performance

* Optimized queries for real-time vote counting.

### 4. Documentation

* Swagger at /api/docs/ is complete and clear.
* This README provides all setup and usage instructions.

---

## Project Structure

text
Copy
Edit
polling_system/
├── polls/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── api_views.py         # API logic including vote trends
│   ├── apps.py
│   ├── models.py            # Models: Question, Choice
│   ├── serializers.py       # DRF serializers
│   ├── tests.py             # Unit tests
│   ├── urls.py              # App-level routing
│   └── views.py             # Traditional Django views
│
├── polling_system/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Root URL routing
│   └── wsgi.py
│
├── templates/               # Optional, if using HTML templates
│   └── polls/
│       └── index.html
│
├── static/                  # Optional static files
│
├── vote_trends.md           # Detailed endpoint doc (custom markdown)
├── requirements.txt         # Installed dependencies
├── README.md                # Project overview & setup guide
├── manage.py

✅ **Project Complete** — All core features, optimizations, and documentation objectives have been met.
