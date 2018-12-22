from flask import Flask, g
from flask_cors import CORS
from helpers.config import Config
from helpers.db_helper import connect_db, connect_redis
from routes.routes import getCount, getPersons

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

@app.before_request
def before_request():
    g.redis_db = connect_redis(app)
    g.db = connect_db(app)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g,'db'):
        g.db.close()

app.register_blueprint(getCount)
app.register_blueprint(getPersons)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    