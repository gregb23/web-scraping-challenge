#set dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars 

#create Flask instance
app = Flask(__name__)

#create mongo connection jusing PyMongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#set route for index.html
@app.route("/")
def home():
    #get data from mongodb
    mars = mongo.db.collection.find_one()

    #return data
    return render_template("index.html", mars=mars)

# set up route for the scrape function
@app.route("/scrape")
def scraper():
    #run scrape function
    scrape_dict = scrape_mars.scrape()

    #update mongo db
    mongo.db.collection.update({}, scrape_dict, upsert=True)

    #go back to home page
    return redirect ("/")

if __name__ == "__main__":
    app.run(debug=True)    