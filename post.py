from flask import Flask,url_for,redirect,render_template, jsonify

app = Flask(__name__)

@app.route("/getData")
def getData():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()