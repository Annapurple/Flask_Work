import secrets
from datetime import datetime
from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from forms.user import RegisterForm
from forms.loginform import LoginForm
from data import db_session
from data.users import User
from data.job import Jobs
from forms.jobform import JobsForm

# base = input()
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
db_session.global_init("db/mars_explorer.db")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def text():
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.user)
    return render_template("main_page.html", job=job, title='Works')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Register form', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = JobsForm()
        job.title = form.title.data
        job.team_leader_id = form.team_leader_id.data
        job.work = form.work.data
        job.collaborator = form.collaborator.data
        job.is_job = form.is_job.data
        job.submit = form.submit.data
        # current_user.job.append(job)
        # db_sess.merge(current_user)
        # db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=form)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
    # db_session.global_init(f"db/mars_explorer.db")
    # session = db_session.create_session()
    # job = Jobs(team_leader=1, job="Mars exploration",
    #             work_size=5, collaborators="1, 2", start_date=datetime.now(), is_finished=False)
    # session.add(job)
    # session.commit()
    # user1 = User(surname="Scott", name="Ridley",
    #              age=21, position="captain", speciality="research engineer",
    #              address="module_1", email="scott_chief@mars.org")
    # user2 = User(surname="Sam", name="Rik",
    #              age=21, position="crew member", speciality="doctor",
    #              address="module_1", email="sam_rik@mars.org")
    # user3 = User(surname="Jane", name="Ron",
    #              age=21, position="crew member", speciality="pilot",
    #              address="module_2", email="jane_ron@mars.org")
    # session.add(user1)
    # session.add(user2)
    # session.add(user3)
    # session.commit()
    # job1 = Jobs(team_leader=1, job="deployment of residential modules 1 and 2",
    #             work_size=15, collaborators="2, 3", start_date=datetime.now(), is_finished=False)
    # session.add(job1)
    # session.commit()
    # for user in session.query(User).filter(User.address == 'module_1'):
    #     print(user)
