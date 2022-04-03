from sqlalchemy import Column, String
from db import *
from _utils import *

class users_banned_db(BASE):
    __tablename__ = "users_banned"
    user_id = Column(String(14), primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id


users_banned_db.__table__.create(checkfirst=True)

@run_in_exc
def is_users_banned(user_id):
    if not str(user_id).isdigit:
        return
    try:
        return SESSION.query(users_banned_db).filter(users_banned_db.user_id == str(user_id)).one()
    except:
        return None
    finally:
        SESSION.close()

@run_in_exc
def add_user_(user_id):
    adder = users_banned_db(str(user_id))
    SESSION.add(adder)
    SESSION.commit()

@run_in_exc
def rm_user(user_id):
    if rem := SESSION.query(users_banned_db).get(str(user_id)):
        SESSION.delete(rem)
        SESSION.commit()

@run_in_exc
def get_all_users_banned():
    rem = SESSION.query(users_banned_db).all()
    SESSION.close()
    return rem