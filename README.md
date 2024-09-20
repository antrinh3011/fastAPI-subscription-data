Install VS code or other IDE : https://code.visualstudio.com/docs/languages/python
Install Python 3.10 : https://www.python.org/downloads/release/python-3100/
Install MySQL Workbench > Connect to mysql and execute the script name : "script_create_schema.sql" to create your database
If you're using the VS code for development. Press Ctrl + Shift + P > Python Create Environment > Create a '.venv' virtual environment in the current workspace
If you're using the VS code for development. You need to access Terminal > New Terminal and install the library list as below.

Install python fastAPI library
>> pip install fastapi uvicorn

Install library to handle Oauth2.0
>> pip install python-jose passlib bcrypt
>> pip install argon2_cffi

Install library to execute MySQL script in async environment
>> pip install sqlalchemy[asyncio] aiomysql pymysql
>> pip install mysql-connector-python

Install "sqlacodegen" to auto generate database table as Model class
>> pip install sqlacodegen

Install setuptools library to support generate Model class from database
>> pip install --upgrade setuptools

Create models class from existing database (please replace your authentication).All database tables will be generated to the "models.py" file
user : root
password : Admin301188
db_name : keywords_subscription
port: 3306
>> sqlacodegen mysql+pymysql://root:Admin301188@localhost:3306/keywords_subscription --outfile models.py

Create library dependencies library for release
>> pip freeze > requirements.txt
>> pip install -r requirements.txt

Running the FastAPI Service
>> uvicorn main:app --reload

Go to url to check the result: http://127.0.0.1:8000/docs

Reference : https://www.fullstackpython.com/object-relational-mappers-orms.html
