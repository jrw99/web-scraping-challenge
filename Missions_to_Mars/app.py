from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask instance
app = Flask(__name__)

# Mongo connection with pyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Home route to render template
@app.route("/")
def home():

    # Find the one record of data from mongo
    mars_data = mongo.db.mars.find_one()

    # Return templated data
    return render_template("index.html", data=mars_data)


# Route for scraping
@app.route("/scrape")
def scrape():

    # ref to mongo 
    mars_record = mongo.db.mars

    # call scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo db
    mars_record.update({}, mars_data, upsert=True)

    # Redirect back home
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
