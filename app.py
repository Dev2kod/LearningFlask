from flask import Flask
app = Flask(__name__)

@app.route('/')
def welcome():
    return'This is my First Flask Project'

if __name__ == '__main__':
    app.run()