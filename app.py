from flask import Flask
app = Flask(__name__)

@app.route('/')
def welcome():
    print('home page rendering')
    return'Flask Project'

@app.route('/users')
def users():
    return'user page'

if __name__ == '__main__':
    app.run(debug=True)
