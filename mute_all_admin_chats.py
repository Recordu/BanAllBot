from sqlalchemy import Column, String
from db import *
from _utils import *

class chats_admins_banned_db(BASE):
    __tablename__ = "chats_admins_banned"
    chats_admin_id = Column(String(14), primary_key=True)

    def __init__(self, chats_admin_id):
        self.chats_admin_id = chats_admin_id


chats_admins_banned_db.__table__.create(checkfirst=True)

@run_in_exc
def is_chats_admins_banned(chats_admin_id):
    if not str(chats_admin_id).isdigit:
        return
    try:
        return SESSION.query(chats_admins_banned_db).filter(chats_admins_banned_db.chats_admin_id == str(chats_admin_id)).one()
    except:
        return None
    finally:
        SESSION.close()

@run_in_exc
def add_chats_admin_(chats_admin_id):
    adder = chats_admins_banned_db(str(chats_admin_id))
    SESSION.add(adder)
    SESSION.commit()

@run_in_exc
def rm_chats_admin(chats_admin_id):
    if rem := SESSION.query(chats_admins_banned_db).get(str(chats_admin_id)):
        SESSION.delete(rem)
        SESSION.commit()

@run_in_exc
def get_all_chats_admins_banned():
    rem = SESSION.query(chats_admins_banned_db).all()
    SESSION.close()
    return rem