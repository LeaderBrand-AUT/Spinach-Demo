# Spinach_Demo

A web application capable of classifying spinach, storing, and retrieving those results.

Requirements:
 - venv
 - Python 3.11.9
 - Docker

How to run:
 - Active virtual environment
    - Windows: .\venv\Scripts\activate
    - macos: source venv/bin/activate

 - Install requirements
    - run 'pip install -r requirements.txt'

 - Activate Docker for database
    - navigate to ./docker
    - run 'docker-compose up'

 - Download and include model
    - Download 'spinach-model-balanced-b.h5' and include it in the ./models/ directory (create if necessary).
    - Downlaod link: https://drive.google.com/file/d/1_T9FOoBlyR80dj4c5M624tZEHlroS1OY/view?usp=sharing
    - If you change the name of this file, make sure to update it in ./scripts/constants.py

 - run 'python app.py' from home directory