# movie-ratings-imdb

## Prerequisites
* Django
* Python3.9.7

## Steps to Setup the Project on Local Device
* git clone git@github.com:sharmakumaraditya/movie-ratings-imdb.git
* change directory to movie-ratings-imdb
* Create a Virtual Environment 
```
virtualenv -p python3 venv
```
* Activate Virtual Environment
```
source venv/bin/activate
```
* Install all the required libraries
```
pip3 install -r requirements.txt
```
* Run the migrations
```
python manage.py makemigrations
```
```
python manage.py migrate
```
* Populate the Data in Database
```
python manage.py populate_db
```
* Start the Server
```
python manage.py runserver
```
* Endpoint to access Admin Portal 
```
/admin
```
* Endpoint to access List of Movies
```
/api/movies
```

## To Run the Test Cases 
```
python manage.py test
```

# Testing the API on Heroku Server
* API to Admin access Of the Portal (by default Admin Portal)
https://moviesimdbrating.herokuapp.com/admin

Login using the username and password provided

* API to Access List of movies : 
https://moviesimdbrating.herokuapp.com/movies

* Accessing List of movies with pagination :
https://moviesimdbrating.herokuapp.com/?search=war&limit=10&offset=0

* Accessing list of movies with Name Filter : 
https://moviesimdbrating.herokuapp.com/movies?search=Psycho

* Accessing list of movies with Genre Filter : 
https://moviesimdbrating.herokuapp.com/movies?search=action

* Accessing list of movies with multiple filters : 
https://moviesimdbrating.herokuapp.com/movies?search=psycho,james

* Accessing list of movies with movie name , director, popularity, imdb rating filter : 
https://moviesimdbrating.herokuapp.com/movies?search=simpsons,Kirkland,90,9


# Handling the Scaling Problem : 

* Database Changes :
    * NoSQL Database can be used or ELK stack can be used
    * Proper indexing of the fields
    * Horizontally Scaling the database
    * Caching the frequently used data for faster responses
    * Using orm queries with selecting only needed fields and ignoring the rest will reduce data traffic

* Infrastructural Changes :
    * If the Application Increases in functionality , Micro Service can be used 
    * Micro Services should be connected using events
    * Proper Error Handling should be done
    * New Relic and elasticsearch to be used faster debugging of issues and proper logging
    * Developing Jenkins and docker Pipeline for faster and procedural deployments 
    * Using Elastic Load Balancer or Elastic Bean Stalk for handling the load ups and down
    * Container management to be done based on the request load

