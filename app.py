from flask import Flask
from update import main as update

app = Flask(__name__)

@app.route('/<string:name>', methods=['GET'])
def hello(name):
    return """
    
    hello 
    """

@app.route('/')
def index():
    return "hello "

if __name__ == "__main__":
    app.run(debug=True)