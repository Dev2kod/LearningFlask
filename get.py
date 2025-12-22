import json
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    user_id = request.args.get('id', None)
    age = 22
    return json.dumps(
        {'name': 'User1',
         "user_id":user_id,
         'password':"1234", 
         "age": age}
            )

@app.route("/show",methods=["POST"])
def vasu():
    data = request.args.get("data","null")
    return json.dumps({
        "data":data
    })

@app.route("/post",methods=["GET","POST"])
def submit():
    data = request.form.get('data','none')
    if request.method=="POST":
        return json.dumps(data)
    return render_template("form.html")

if __name__ == '__main__':
    app.run(debug=True)