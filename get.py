from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/logging", methods=["GET", "POST"])
def logging():
    if request.method == "POST":
        name = request.form.get("name", "Guest")
        return f"Hello, {name}"
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
