from flask import Flask
import os
app = Flask(__name__)


@app.route('/')
def hello():
    content = os.popen("ls ~").read()
    return content


if __name__ == '__main__':
    app.run()