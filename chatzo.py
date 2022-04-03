import threading
from sqlalchemy import func, distinct, Column, String, UnicodeText
from db import *
from _utils import *


class bdlistFilters(BASE):
    __tablename__ = "bdlist"
    user_id = Column(String(14), primary_key=True)
    chat_id = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, user_id, chat_id):
        self.user_id = str(user_id)  
        self.chat_id = str(chat_id)

    def __eq__(self, other):
        return bool(isinstance(other, bdlistFilters)
                    and self.user_id == other.user_id
                    and self.chat_id == other.chat_id)


bdlistFilters.__table__.create(checkfirst=True)

bdlist_FILTER_INSERTION_LOCK = threading.RLock()

CHAT_bdlistS = {}

@run_in_exc
def add_to_bdlist(user_id, chat_id):
    with bdlist_FILTER_INSERTION_LOCK:
        bdlist_filt = bdlistFilters(str(user_id), chat_id)

        SESSION.merge(bdlist_filt)  # merge to avoid duplicate key issues
        SESSION.commit()
        CHAT_bdlistS.setdefault(str(user_id), set()).add(chat_id)

@run_in_exc
def get_chat_bdlist(user_id):
    return CHAT_bdlistS.get(str(user_id), set())


def num_bdlist_filters():
    try:
        return SESSION.query(bdlistFilters).count()
    finally:
        SESSION.close()


def num_bdlist_chat_filters(user_id):
    try:
        return SESSION.query(bdlistFilters.user_id).filter(bdlistFilters.user_id == str(user_id)).count()
    finally:
        SESSION.close()


def num_bdlist_filter_chats():
    try:
        return SESSION.query(func.count(distinct(bdlistFilters.user_id))).scalar()
    finally:
        SESSION.close()


def __load_chat_bdlists():
    global CHAT_bdlistS
    try:
        chats = SESSION.query(bdlistFilters.user_id).distinct().all()
        for (user_id,) in chats:  #
            CHAT_bdlistS[user_id] = []
        all_filters = SESSION.query(bdlistFilters).all()
        for x in all_filters:
            CHAT_bdlistS[x.user_id] += [x.chat_id]
        CHAT_bdlistS = {x: set(y) for x, y in CHAT_bdlistS.items()}
    finally:
        SESSION.close()


__load_chat_bdlists()