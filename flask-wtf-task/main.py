from flask import Flask, url_for, render_template, request, redirect
from forms.loginform import LoginForm

app = Flask(__name__, )
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("form.html", form=form, title='Авторизация')


@app.route('/load_photo', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return render_template('photo_form.html')
    elif request.method == 'POST':
        f = request.files['file']
        with open("./static/images/temp/file.png", "wb") as file:
            file.write(f.read())
        return redirect(url_for('sample_file_upload'), 301)


@app.route('/carousel')
def carousel():
    return render_template('carousel_photo.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
