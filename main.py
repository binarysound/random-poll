import configparser
import random
import string
from optparse import OptionParser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

parser = OptionParser()
parser.add_option("-c", "--config", dest="config", help="configuration file")

(options, _) = parser.parse_args()

config_file = options.config if options.config else "dev.cfg"

config = configparser.ConfigParser()
config.read(config_file)

db_config = config["database"]

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://%s:%s@%s/%s" % (
        db_config["user"],
        db_config["password"],
        db_config["host"],
        db_config["database"]
    )
)
db = SQLAlchemy(app)

app_config = config["app"]
host = "0.0.0.0"
port = 80

if app_config:
    if app_config["host"]:
        host = app_config["host"]
    if app_config["port"]:
        port = app_config["port"]


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return "<Question %r>" % self.content


@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    app.run(host=host, port=port)
