from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def text():
    return 'Миссия колонизация марса'


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    param = {}
    param['title'] = title
    return render_template('base.html', **param)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
