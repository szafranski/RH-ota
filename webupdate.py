import flask
import subprocess
from time import sleep
import os

app = flask.Flask(__name__)

@app.route('/yield')
def index():
    def inner():
        content = os.popen("htop").read()
        for line in content:
            yield line.rstrip() + '<br/>\n'
        # proc = subprocess.Popen(['htop'],shell=True,stdout=subprocess.PIPE)
        # for line in iter(proc.stdout.readline,''):
        #     yield line.rstrip() + '<br/>\n'

    return flask.Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show th$

app.run()