from flask import Flask, url_for, render_template

app = Flask(__name__, template_folder='templates1')
list_prof = ['Инженер-исследователь', 'Инженер жизнеобеспечения', 'Киберинженер', 'Пилот', 'Строитель', 'Экзобиолог', 'Врач', 'Метеоролог', 'Астрогеолог', 'Климатолог']

@app.route('/list_prof/<par>')
def index(par):
    param = {}
    param['headline'] = "Миссия Колонизация Марса"
    param['text'] = "И на Марсе будут яблони цвести!"
    param['list_prof'] = list_prof
    param['par'] = par
    return render_template('base1.html', **param)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)