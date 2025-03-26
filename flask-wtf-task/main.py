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


@app.route('/training/<prof>')
def training(prof):
    param = {}
    param['prof'] = prof
    return render_template('sample_training.html', **param)


@app.route('/list_prof/<par>')
def list_pro(par):
    list_prof = ['Инженер-исследователь', 'Инженер жизнеобеспечения', 'Киберинженер', 'Пилот', 'Строитель',
                 'Экзобиолог', 'Врач', 'Метеоролог', 'Астрогеолог', 'Климатолог']
    param = {}
    param['list_prof'] = list_prof
    param['par'] = par
    return render_template('pro_list.html', **param)


@app.route('/answer')
@app.route('/auto_answer')
def ans():
    d = {}
    d['title'] = "Анкета"
    d['surname'] = "Watny"
    d['name'] = "Mark"
    d['education'] = "выше среднего"
    d['profession'] = "штурман марсохода"
    d['sex'] = "male"
    d['motivation'] = "Всегда мечтал застрять на Марсе!"
    d['ready'] = "True"
    return render_template('auto_answer.html', **d)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
