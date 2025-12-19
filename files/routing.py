from flask import Flask,redirect,url_for
app = Flask(__name__)

@app.route('/')
def home():
    return'this is homepage'

@app.route('/success/<int:score>')
def passed(score):
    return f"this person has passed with {score} marks"

@app.route('/fail/<int:score>')
def failed(score):
    return "<html><body><h1>Person has failed</h1></body></html>"

@app.route('/result/<int:score>')
def result(score):
    result=""
    if score<50:
        result="fail"
        return redirect(url_for('failed',score=score))
    else:  
        result="success"
        return redirect(url_for('passed',score=score))


if(__name__=='__main__'):
    app.run(debug=True)