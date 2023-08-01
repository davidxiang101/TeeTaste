# TeeTaste
👕🚀 An AI-powered T-shirt recommendation platform built with NextJS, Django and TensorFlow.

## Overview
TeeTaste is a personalized T-shirt recommendation engine. It allows users to vote between two T-shirts, and based on the user's preferences, it will recommend a new pair of T-shirts to vote on. The aim is to create a more interactive and personalized shopping experience for T-shirt enthusiasts, reducing the cognitive load of choosing from hundreds of T-shirts.

The motivation behind this project is to use modern machine learning techniques to enhance the user's shopping experience by creating a recommendation system based on a user's individual tastes and preferences. It is designed to be an enjoyable and interactive way of discovering new T-shirts without having to manually search through the entire product catalog.


## Technologies Used
Frontend: Next, Tailwind
Backend: Django
Database: SQLite (Local development), PostgreSQL (Production)

## Set Up
Here are the steps to set up the project locally for development:

1. **Clone the repository**:

git clone https://github.com/davidxiang101/TeeTaste.git
cd TeeTaste


2. **Install the dependencies**:

- For the Django backend:
  ```
  pip install -r requirements.txt
  ```
- For the React frontend:
  ```
  cd client
  npm install
  ```

3. **Prepare the Django database**:

- Run migrations to prepare your database:
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

- Load T-shirt images to your database using the provided script:
  ```
  python load_images_to_database.py
  ```

4. **Run the servers**:

- For the Django backend:
  ```
  python manage.py runserver
  ```
- For the React frontend:
  ```
  cd client
  npm start
  ```

The application will be available at `http://localhost:3000`.

Please note that this guide is intended for development only. The production deployment might require additional steps such as setting up a cloud-based database, configuring a production web server, etc. 


Please note that this guide is intended for development only. The production deployment might require additional steps such as setting up a cloud-based database, configuring a production web server, etc.

Enjoy using TeeTaste!
