from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('flask-test.html')
    if request.args:
        name = request.args['name']
        age = request.args['age']
        st = True if 'student' in request.args else False
        return render_template('greeting.html', name=name, age=age, student=st)

if __name__ == '__main__':
    app.run()
