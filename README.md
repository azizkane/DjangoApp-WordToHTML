# Django REST API for Word to HTML Conversion

This application is a Django REST API designed to convert Word documents into accessible HTML pages as faithfully as possible.

## Prerequisites

- Python 3.9
- Django
- Django REST Framework
- python-docx (for reading Word documents)
- any other necessary libraries for HTML conversion

## Installation

1. **Clone the repository:**


    git clone 


2. **Create and activate a virtual environment:**


    `python -m venv env`
    `source env/bin/activate`  # On Windows use `env\Scripts\activate`


3. **Install the required packages:**


    pip install -r requirements.txt


## Configuration

1. **Database setup:**

    `cd app`
    Configure your database settings in `settings.py`. By default, Django uses SQLite.

2. **Migrate the database:**


    python manage.py migrate


3. **Run the server:**


    python manage.py runserver


## API Endpoints

- **Convert Word to HTML:**

    - **URL:** `/api/convert/`
    - **Method:** `POST`
    - **Payload:** A Word document file
    - **Response:** HTML content

- **List Converted Documents:**

    - **URL:** `/api/documents/`
    - **Method:** `GET`
    - **Response:** List of converted documents with metadata

- **Retrieve Converted Document:**

    - **URL:** `/api/documents/<id>/`
    - **Method:** `GET`
    - **Response:** HTML content of the specified document

- **Delete Converted Document:**

    - **URL:** `/api/documents/<id>/`
    - **Method:** `DELETE`
    - **Response:** Confirmation of deletion

## Usage

1. **Start the server:**


    python manage.py runserver


2. **Use an API client (like Postman) or a frontend to send a POST request to `/api/convert/` with a Word document file.

3. **Receive the HTML content as a response.**


| Author  | Date       | email|
|---------|---------------|--------|
| Aziz Kane  | 09/10/2023  |[aziukane@gmail.com](mailto:aziukane@gmail.com)|


## Notes

- Ensure that your Word documents are well-formatted for the best conversion results.
- You may need to adjust the conversion logic to handle specific formatting or content types.
