# Capstone Project Comic Management API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [python-jose](https://pypi.org/project/python-jose/) library used to work with JSON Web Tokens(JWT)

## Database Setup
With Postgres running, restore a database using the initdb.psql file provided. From the backend folder in terminal run:
```bash
createdb comiquea
psql comiquea < initdb.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

There are two different ways of configure the server:

- First way: exceute

```bash
export DATABASE_URL='postgresql://jbossini:torm3nta@localhost:5433/comiquea'
export FLASK_ENV='development'
export FLASK_APP='app.py'
export FLASK_RUN_PORT=8080
export FLASK_RUN_HOST=0.0.0.0
export AUTH0_DOMAIN='jbossini.eu.auth0.com'
export ALGORITHMS='RS256'
export API_AUDIENCE='comiquea-api'
export REDIRECT_URL='http://192.168.1.111:8080'
export CLIENT_ID='<your client Id from Auth 0>'
export RESULTS_PER_PAGE=10
export EDITOR_AUTHORIZATION_TOKEN='<Valid token for editor role>'
export FAN_AUTHORIZATION_TOKEN='<Valid token for fan role>'
export WRITER_AUTHORIZATION_TOKEN='Valid Token for writer role>'

flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


- Second way : A file named setup.sh is provided containing the export sentences from above, you can use it and fill it with the appropiate information and then execute it : 

```bash
 chmod +x setup.sh
. setup.sh
```

## Testing 

To running the test correctly, first you should truncate the database and recreate it. To do so, you just have to execute the following sentences in a bash terminal from the backend folder: 

```bash
psql comiquea<initdb.sh
```
## API Reference

### Getting started
- Base URL: At this moment this API works in your local machine in the port setted up in your setup.sh file , so the base URL for our API is  http://127.0.0.1:FLASK_RUN_PORT and also it is deployed on Heroku in this URL: https://comiquea.herokuapp.com
- Authentication : This version of the API require authentication with Auth 0

### Endpoints

Note: Sample URLs always contain the minimum Authentication token in order to access to the information

GET '/'
- Return the status of the server
- Request Arguments: None
- Sample URL : curl http://localhost:port/
- Returns : The string API is running and healthy

GET '/editorials'
- Fetches a complete set of Comic Editorials from the database
- Request Arguments: None needed but you can use the parameter page if you want to paginate the response
- Sample URL : curl -H "Authorization: Bearer $FAN_AUTHORIZATION_TOKEN" https://comiquea.herokuapp.com/editorials
- Returns: 
  -An object JSON with a list of editorials in our database and also the flag success and the number of registries obtained 
 
```json
{
  "editorials": [
    {
      "address": "New York", 
      "id": 1, 
      "mail": "marvel-comics@marvel.comics", 
      "name": "Marvel"
    }, 
    {
      "address": "New York", 
      "id": 2, 
      "mail": "dc-comics@marvel.comics", 
      "name": "DC"
    }
  ], 
  "success": true, 
  "total_editorials": 2
}
```
GET '/editorials/<id_editorial>'
- Fetches a specific editorial from our database if exists
- Request Arguments: the id of the editorial 
- Sample URL : curl -H "Authorization: Bearer $FAN_AUTHORIZATION_TOKEN" https://comiquea.herokuapp.com/editorials/<id_editorial>
- Returns:
  - An object JSON with the editorial in our database
  - success Flag(True if everything went right)
 
```json
{
  "editorial": {
    "address": "New York", 
    "id": 1, 
    "mail": "marvel-comics@marvel.comics", 
    "name": "Marvel"
  }, 
  "success": true
}
```

POST '/editorials'
- Create a new Editorial in our database
- Required Arguments: None
- Sample URL : curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $EDITOR_AUTHORIZATION_TOKEN" https://comiquea.herokuapp.com/editorials -d '{"name": "Editorial name", "address": "location of the Editorial", "mail": "mail@editorial.com"}'
- Returns :
    - The id of the new Editorial created
    - success Flag(True if everything went right)
- Sample:
```json
{
  "id_editorial": 4, 
  "success": true
}
```

DELETE '/editorials/<id_editorial>'
- Delete an Editorial from the database (and the series and comics related to this Editorial)
- Request Arguments: The id in the url of the Editorial to delete
- Sample URL : curl -X DELETE -H "Authorization: Bearer $EDITOR_AUTHORIZATION_TOKEN" https://comiquea.herokuapp.com/editorials/<id_editorial>
- Returns :
    - id of the deleted editorial
    - the flag success (True if everything went right)
- Sample :
```json
{
  "id_editorial": 4, 
  "success": true
}
```

PATCH '/editorials/<id_editorial>'
- Create a new Editorial in our database
- Required Arguments: The id in the url of the Editorial to update
- Sample URL : curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer $EDITOR_AUTHORIZATION_TOKEN" https://comiquea.herokuapp.com/editorials/<id_editorial> -d '{"name": "Editorial name", "address": "location of the Editorial", "mail": "mail@editorial.com"}'
- Returns :
    - An object with the updated editorial
    - success Flag(True if everything went right)
- Sample:
```json
{
  "editorial": {
    "address": "location of the Editorial", 
    "id": 3, 
    "mail": "mail@editorial.com", 
    "name": "Editorial name"
  }, 
  "success": true
}
```


## Authors
José Manuel Díaz Bossini
## Acknowledgements
To my family and collegues for their patience with me . To all the teachers from this course for sharing their knowledge with us.

