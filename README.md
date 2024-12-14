# Quizy - The Quiz App

Welcome to Quizy! This is a Django-based web application that allows users to take quizzes, view their results, and track their progress. The application supports multiple-choice questions and provides a user-friendly interface for both taking quizzes and viewing results.

The application can be accessed at https://quizy-oe3t.onrender.com/


## Features

- User authentication (login, registration, logout)
- Create and manage quiz sessions
- Multiple-choice questions with single or multiple correct answers
- View detailed quiz results
- Responsive design using Bootstrap


## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.8+
- Git

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/saurabh228/quizy.git
   cd quizy
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the project root and add the following environment variables:

   ```sh
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Apply migrations:**

   ```sh
   python manage.py migrate
   ```

6. **Create a superuser:**

   ```sh
   python manage.py createsuperuser
   ```


7. **Run the development server:**

   ```sh
   python manage.py runserver
   ```

   The application will be available at `http://127.0.0.1:8000/`.

## Project Structure

- 


- `quizy`: Main project directory
  - `settings.py`: Project settings
  - `urls.py`: URL configuration
  - `wsgi.py`: WSGI configuration
- `quiz/`: Quiz app directory
  - `models.py`: Database models
  - `views.py`: Application views
  - `urls.py`: URL configuration for the quiz app
  - `templates/quiz/`: HTML templates
  - `templates/registration/`: HTML templates for authentication
- `requirements.txt`: Project dependencies

## How It Works

### User Authentication

- Users can register, log in, and log out.
- Authentication is required to start a quiz or view results.

### Quiz Sessions

- Users can start a new quiz session by selecting the number of questions.
- Each session is tracked, and users can resume incomplete sessions.

### Questions and Answers

- Questions are multiple-choice with single or multiple correct answers.
- Users can submit answers and receive immediate feedback.

### Results

- Users can view detailed results of completed quizzes.
- Results include the score, correct answers, and user-selected answers.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Contact

For any questions or feedback, please contact [Saurabh Saini](https://github.com/saurabh228).
