from datetime import datetime

from flask import Flask
from data import db_session
from data.users import User
from data.job import Jobs


base = input()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

if __name__ == '__main__':
    db_session.global_init(f"db/{base}")
    session = db_session.create_session()
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
    for user in session.query(User).filter(User.address == 'module_1'):
            print(user)