# VocApp - What is this?
Basic vocabulary trainer mobile web app built in Flask runs on SQLite database
Demo: http://vocapp.pythonanywhere.com/

# Instalation
1. Download or clone repository
2. Create a virtual enviroment for the app (Open terminal in the project folder and us a comand: virtualenv venv)
3. Activate the venv with command: . venv/bin/activate
4. Install all required packages with: pip install -r requirements.txt
5. Run export command: export FLASK_APP=vocapp.py
6. Set database path and file in main app file vocapp.py
7. To initilize a database use command: flask db init
8. To to create and migrate a database: flask db migrate
9. After migration use: flask db upgrade to save changes is the database
