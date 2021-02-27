from flask import Flask, render_template, redirect
import pymongo
import scrape_mars, config

app = Flask(__name__)

# setup mongo connection
client = pymongo.MongoClient(config.mongo_conn)

# connect to mongo db and collection
db = client.mars_db
collection = db.mars_collection


@app.route("/")
def index():
    mars_data = collection.find_one()
    return render_template("index.html", mars_data=mars_data)

"""
@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = scrape_craigslist.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)

"""
if __name__ == "__main__":
    app.run(debug=True)
