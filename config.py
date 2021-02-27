# The name of the database you are connecting to
db_name="mars_db"

# IF USING ATLAS (CLOUD) THE CONNECTION STRING IS AS FOLLOWS
# THIS CAN BE FOUND WHEN YOU LOGIN TO YOUR ATLAS ACCOUNT
# mongo_conn="mongodb+srv://melissa:teame@cluster0.4dt6k.mongodb.net/test?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
# IF USING LOCAL HOST THE CONNECTION STRING WILL BE AS FOLLOWS
mongo_conn="mongodb://localhost:27017"
pg_username = "melissa"
pg_password = "teame"



# debug true will print extra output
debug=False

# For future development to allow for using local data files to test 
# before scraping website.
test=True

#colors
greenblue = '#097392'
lightgreen = '#83B4B3'
lightyellow = '#FFF0CE'
orangered = '#D55534'
dark = '#383838'

# page range
url_page_range = 1