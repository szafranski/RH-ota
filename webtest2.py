from flask import Flask
import os
app = Flask(__name__)
import subprocess


@app.route('/')
def hello():
    to_show = []
    content = subprocess.Popen(['htop'],shell=True,stdout=subprocess.PIPE)
    for line in content:
        for line in iter(proc.stdout.readline,''):
            yield line.rstrip() + '<br/>\n'

    to_show = ('\n\t\t'.join(to_show))

    return to_show


if __name__ == '__main__':
    app.run()