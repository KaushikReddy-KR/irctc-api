
# SDE API Round - IRCTC

This project is a Django-based Railway Management System. It allows users to:
- **Register** and **login**.
- **Check train availability** between two stations.
- **Book a seat** on a train (with concurrency handling).
- **View booking details**.

## Table of Contents

- [Features](#features)
- [Assumptions](#assumptions)
- [Setup](#setup)
- [Testing](#testing)

## Features
- **User Authentication**: Register and login with Django’s built-in User model and DRF TokenAuthentication.
- **Train Management**: Admins can add trains with a source, destination, total seats, and a unique train number.
- **Booking System**: Concurrent seat booking is handled with Django transactions and row-level locking (`select_for_update`).
- **Seat Availability**: Users can query available seats between any two stations.

---

## Assumptions

- **Database**: The project uses SQLite for development. In a production environment, consider PostgreSQL or MySQL.
- **API Key**: The admin API key is defined in `settings.py` (or via an environment variable) as `ADMIN_API_KEY`.
---

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/KaushikReddy-KR/irctc-api.git
   cd railway-irctc
   ```

2. **Create and activate the Virtual Environment**
    ```bash
    python3 -m venv railwayenv
    .\railwayenv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Running the Server**
    ```bash
    python manage.py runserver
    ```

## Testing:
Testing can be done manually using postman with the API endpoints provided below:

- **User Registration:** `POST /api/register/`  
  **Payload:**
  ```json
  {
      "username": "your_username",
      "email": "your_email@example.com",
      "password": "your_password"
  }
  ```

    Upon success we get a message `User registered successfully`.

    **Test Using curl:**
    ```bash
    curl --location 'http://127.0.0.1:8000/api/register/' \ 
    --header 'Content-Type: application/json' \
    --data-raw '{
    "username": "kaushik12",
    "email": "kaushik12@gmail.com",
    "password": "test123"
    }'
    ```

- **User Login:** `POST /api/login/`  
  **Payload:**
  ```json
  {
  "username": "john_doe",
  "password": "strongpassword"
  }

  ```

    Upon success a JSON response containing a token is generated .

    **Test Using curl:**
    ```bash
   curl --location 'http://127.0.0.1:8000/api/login/' \
   --header 'Content-Type: application/json' \
   --data '{
    "username": "kaushik",
    "password": "test123"
    }'
    ```

- **Add Train** `POST /api/admin/add-train/`  
  **Headers:**

  Include the token you received from login:
  ```http
  Authorization: Token your_user_token
  ```

  **Payload:**
  ```json
  {
  "train_no": "12345",
  "name": "Express",
  "source": "CityA",
  "destination": "CityB",
  "total_seats": 100
  }


  ```

    Upon success the train is created and the response returns the new train details.

    **Test Using curl:**
    ```bash
   curl --location 'http://127.0.0.1:8000/api/admin/add-train/' \
   --header 'API-KEY: railway-api-123' \
   --header 'Content-Type: application/json' \
   --data '{
    "train_no":"12456",
    "name": "Express 102",
    "source": "CityA",
    "destination": "CityB",
    "total_seats": 100,
    "available_seats":100
    }'
    ```

- **Check Train Availability:** `GET /api/trains/?source=CityA&destination=CityB`  

    Upon success a list of trains that operate between CityA and CityB, with each train’s available seats is given.

    **Test Using curl:**
    ```bash
   curl --location 'http://localhost:8000/api/trains/?source=CityA&destination=CityB'
    ```

- **Book a Seat** `POST /api/book/`  

    **Headers:**

    Include the token you received from login:
    ```http
    Authorization: Token your_user_token
    ```
    **Payload:**
    ```json
    {
  "train_id": "12345"
  }

    ```
   A booking is created (HTTP 201) if a seat is available; if no seats are available, you should see an error (HTTP 400).


- **Get Booking Details:** `GET /api/booking/<booking_id>`  

    **Headers:**

    Include the token you received from login:
    ```http
    Authorization: Token your_user_token
    ```

   Upon success the details of the specified booking if it belongs to the logged-in user.

    **Test Using curl:**
    
    Note: Please replace the token with the token you receive at the time of login.
    ```bash
   curl --location 'http://127.0.0.1:8000/api/booking/1' \
   --header 'Authorization: Token e89ca627b1b86dba3bf4a3d880bd2fd506ef360d'
    ```

- **Testing Concurrency :**

    To ensure that multiple users cannot book the same seat simultaneously, you can simulate concurrent requests.

    Run the script.py present in the folder. 
    Please remember this will only work when the `available_seats` is set to 1 otherwise both the users get assigned to different seats.
    **Note**: Replace the token values of both the user tokens with the one you get during login.
    ```bash
    python script.py
    ```
    Upon success only one booking should succeed (HTTP 201) and the other will fail (HTTP 400 with an error message `"No seats available"`).
