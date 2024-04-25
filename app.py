from flask import Flask  # , jsonify, request
import psycopg2
from config import load_config

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello flask"


@app.route("/query_db", methods=["GET"])
def query_get():
    pass


if __name__ == "__main__":
    app.run(debug=True)
