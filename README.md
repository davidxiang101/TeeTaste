# TeeTaste
👕🚀 An AI-powered T-shirt and Sneaker recommendation engine built with NextJS, Django and TensorFlow.

## Overview
TeeTaste is a personalized T-shirt recommendation engine. It allows users to vote between two T-shirts, and based on the user's preferences, it will recommend a new pair of T-shirts to vote on. The aim is to create a more interactive and personalized shopping experience for T-shirt enthusiasts, reducing the cognitive load of choosing from hundreds of T-shirts.

The motivation behind this project is to use modern machine learning techniques to enhance the user's shopping experience by creating a recommendation system based on a user's individual tastes and preferences. It is designed to be an enjoyable and interactive way of discovering new T-shirts without having to manually search through the entire product catalog.

## How TeeTaste Finds Similar T-Shirts

TeeTaste uses a combination of machine learning techniques to provide a fun and interactive way to discover T-shirts that match your taste. The following is a high-level overview of the process:

1. **Feature Extraction**:

   TeeTaste uses a technique known as feature extraction to represent each T-shirt image as a numerical vector. It does this by leveraging a pre-trained deep learning model called ResNet.

   ResNet, short for Residual Network, is a type of Convolutional Neural Network (CNN) that has been trained on a massive dataset (ImageNet). It has learned to recognize various low-level features (like lines, curves, colors) and high-level features (like shapes, objects) from this dataset.

   We use ResNet to process each of our T-shirt images. The output is a feature vector that represents the key visual characteristics of the T-shirt. These feature vectors serve as input for the next step.
   
2. **Cosine Similarity**:

   Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them. The cosine of 0° is 1, and it is less than 1 for any angle in the interval (0, π] radians. 

   It is thus a judgment of orientation and not magnitude: two vectors with the same orientation have a cosine similarity of 1, two vectors at 90° have a similarity of 0, and two vectors diametrically opposed have a similarity of -1, independent of their magnitude. 

   By using cosine similarity, we can effectively determine how similar two T-shirts are based on their visual features.

3. **Approximate Nearest Neighbors**:

   After transforming all T-shirt images into feature vectors, we want to find the ones that are most similar to a selected T-shirt. For this, we use a technique called Approximate Nearest Neighbors (ANN).

   ANN allows us to quickly search through our dataset for vectors that are close to a given vector. The way we determine "closeness" is by using a measure called cosine similarity.

In this way, TeeTaste combines these techniques to provide an interactive tool that adapts to your T-shirt preferences and provides increasingly tailored recommendations.





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
- For the NextJS frontend:
  ```
  cd tee-taste-frontend
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
  python import_images.py
  ```

4. **Run the servers**:

- For the Django backend:
  ```
  python manage.py runserver
  ```
- For the NextJS frontend:
  ```
  cd tee-taste-frontend
  npm run dev
  ```

The application will be available at `http://localhost:3000`.

Please note that this guide is intended for development only. The production deployment might require additional steps such as setting up a cloud-based database, configuring a production web server, etc. 


Please note that this guide is intended for development only. The production deployment might require additional steps such as setting up a cloud-based database, configuring a production web server, etc.

Enjoy using TeeTaste!
