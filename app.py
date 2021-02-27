from flask import Flask, render_template, redirect
import pymongo
import mission_to_mars.scrape_mars
import mission_to_mars.config
app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db
collection = db.mars_collection


@app.route("/")
def index():
    listings = collection.find_one()
    return render_template("index.html", listings=listings)

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
