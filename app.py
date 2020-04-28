from flask import Flask
from update import app_update as update

app = Flask(__name__)

@app.route('/')
def index():
    return update

if __name__ == "__main__":
    app.run(debug=True, port=5050)