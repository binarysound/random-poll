import random
import string
from optparse import OptionParser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

parser = OptionParser()
parser.add_option("-e", "--env", dest="env", help="environment configuration file")

(options, _) = parser.parse_args()

env_file = options.env if options.env else ".env"

class EnvParser(object):
    def __init__(self):
        pass

    def parse(self, env_file):
        env = {}
        with open(env_file, "r") as f:
            for line in f:
                if line[0] == "#": pass  # This is comment line
                parsed = line.strip().split("=")
                if len(parsed) != 2:
                    print("Ill-formed .env file")
                    exit(1)
                env[parsed[0]] = parsed[1]
        return env

env_parser = EnvParser()
env = env_parser.parse(env_file)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://%s:%s@%s/%s" % (
        "postgres",
        env["DB_PASSWORD"],
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
