# Nexu Backend Coding Exercise

## Overview

This project is a backend application built for an existing frontend, as part of the Nexu Backend Coding Exercise. The goal is to demonstrate your ability to create robust and efficient endpoints using Django and Django REST Framework. The project includes endpoints to list, create, and update brands and car models.
The required endpoints are:

- **GET /brands**: List all brands. The average price for each brand is calculated as the average of its models' average prices.
- **GET /brands/:id/models**: List all models for a specific brand.
- **POST /brands**: Create a new brand. The brand name must be unique.
- **POST /brands/:id/models**: Create a new model for a specific brand. The model name must be unique within that brand and, if provided, the average price must be greater than 100,000.
- **PUT /models/:id**: Update the average price of a model. The average price must be greater than 100,000.
- **GET /models?greater=&lower=**: List all models. If the `greater` parameter is included, only models with an average price greater than the parameter are returned. If the `lower` parameter is included, only models with an average price lower than the parameter are returned.

## Database

The application uses Django's default database (SQLite) for development. The database is populated from the `models.json` file included in the repository using a custom management command.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/julia-sartirana/nexu-backend.git
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
    python manage.py makemigrations
    python manage.py migrate
   ```
5. **Populate the database:**
   ```bash
    python manage.py populate_data
   ```
6. **Run the development server:**
   ```bash
    python manage.py runserver
   ```

## Testing

The project includes tests to ensure that the endpoints and logic work correctly. To run the tests, execute:

```bash
python manage.py test
```

## Thought Process and Notes
* The project uses Django REST Framework's generic views and ModelSerializers to minimize boilerplate code and keep the codebase clean.
* The data import process is optimized by using bulk_create to reduce the number of database hits.
* The endpoints have been built according to the exercise requirements, with appropriate validations to ensure data integrity.
* Although SQLite is used for this exercise, for a production scenario I would recommend using PostgreSQL for improved performance and scalability.
* Future improvements could include adding pagination to the endpoints returning large datasets and expanding the test suite.