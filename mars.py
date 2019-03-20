from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_info = mongo.db.mars_info.find_one()
    # Return template and data
    return render_template("index.html", mars_info = mars_info)

@app.route('/scrape')
def scape():

    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.hemispheres()
    mars_info.update({}, mars_data,upsert = True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)