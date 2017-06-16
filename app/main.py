import random
import string
from optparse import OptionParser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

parser = OptionParser()
parser.add_option("-p", "--db-password", dest="db_password", help="password of database")

(options, _) = parser.parse_args()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://%s:%s@%s/%s" % (
        "postgres",
        options.db_password,
        "postgres",
        "postgres"
    )
)
db = SQLAlchemy(app)

host = "0.0.0.0"
port = 80

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
