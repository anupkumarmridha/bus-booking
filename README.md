## Steps to Run the Project:

1. Clone the project int your local machine.<br />
2. Open the project folder and run the following commands inside the terminal: <br />
    `python -m venv env`<br />
    `env/Scripts/activate`<br />
    `pip install -r requirements.txt`<br />
    `python manage.py makemigrations`<br />
    `python manage.py migrate`<br />
    `python manage.py createsuperuser`<br />
3. This will ask you for the Username, Email, and password for the superuser<br />
&emsp; Username: admin<br />
&emsp; Email: admin@gmail.com<br />
&emsp; **Note** : The username, email and password can be different.<br />
4. Run command: `python manage.py runserver`<br />
5. This will start the local server where you can see the web app running.<br />