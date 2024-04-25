from flask import Flask, request, render_template  # , jsonify
from query import query_series, query_parents_guide

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# Itt majd a frontendnek kéne küldenie adatot, amit a request.get()-en keresztül az args-hoz rendelünk
@app.route("/query-data")  # , methods=["GET"]
def query_get():
    # args = request.get()  # itt majd az args-al kell csinálni a query-t

    df = query_series("Game of Thrones")

    return df


if __name__ == "__main__":
    app.run(debug=True)
