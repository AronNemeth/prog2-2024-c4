from flask import Flask, request, render_template  # , jsonify
from queries import q_series, q_parents_guide

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# Itt majd a frontendnek kéne küldenie adatot, amit a request.get()-en keresztül az args-hoz rendelünk
@app.route("/process_request", methods=["GET"])
def query_get():
    args = request.args  # itt majd az args-al kell csinálni a query-t

    # df = query_series("Game of Thrones")

    return args


if __name__ == "__main__":
    app.run(debug=True)
