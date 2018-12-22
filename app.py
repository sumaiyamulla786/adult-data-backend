from flask import Flask, g
from flask_cors import CORS
from helpers.config import Config
from helpers.db_helper import connect_db, connect_redis
from routes.routes import adult_data

app = Flask(__name__)

#enable cors for local development
CORS(app)

#setting the config for app
app.config.from_object(Config)

# setting mongo client and redis client on request context using two connector functions
@app.before_request
def before_request():
    g.redis_db = connect_redis(app)
    g.db = connect_db(app)

# closing db on request teardown
@app.teardown_request
def teardown_request(exception):
    if hasattr(g,'db'):
        g.db.close()

# register blueprint for adult_data endpoints
app.register_blueprint(adult_data)

# bootstraping the app
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    