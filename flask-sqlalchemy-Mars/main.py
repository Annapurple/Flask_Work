import secrets
from datetime import datetime
from flask import Flask, render_template, redirect, abort, request
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from forms.user import RegisterForm
from forms.loginform import LoginForm
from data import db_session
from data.users import User
from data.job import Jobs
from data.departments import Department
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
    jobs = db_sess.query(Jobs).all()
    new_jobs = []
    for job in jobs:
        j = job.to_dict(only=["id", "team_leader", "work_size", "collaborators", "is_finished", "job"])
        tl = db_sess.query(User).filter(User.id == j["team_leader"]).first()
        j["team_leader"] = tl.name + " " + tl.surname
        j["id"] = tl.id
        j["work_size"] = job.work_size
        j["collaborators"] = job.collaborators
        j["is_finished"] = job.is_finished
        j["job"] = job.job
        new_jobs.append(j)
    return render_template("main_page.html", job=new_jobs, title='Works')


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
        job = Jobs(
            job=form.title.data,
            team_leader=form.team_leader_id.data,
            work_size=form.work.data,
            collaborators=form.collaborator.data,
            start_date=datetime.now(),
            is_finished=False)
        if job:
            current_user.job.append(job)
            db_sess.merge(job)
            db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=form)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.title.data = jobs.job
            form.team_leader_id.data = jobs.team_leader
            form.work.data = jobs.work_size
            form.collaborator.data = jobs.collaborators
            form.collaborator.data = jobs.collaborators
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.job = form.title.data
            jobs.team_leader = form.team_leader_id.data
            jobs.work_size = form.work.data
            jobs.collaborators = form.collaborator.data
            jobs.is_finished = form.is_job.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
    # db_session.global_init(f"db/mars_explorer.db")
    # session = db_session.create_session()
    # app.run(host='127.0.0.1', port=8080)
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
