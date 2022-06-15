import pickle
import threading
from sqlalchemy import Column, Integer, LargeBinary
from pyrobot.helper_functions.sql_helpers import BASE, SESSION


class gDriveCreds(BASE):
    __tablename__ = "gDrive"
    chat_id = Column(Integer, primary_key=True)
    credential_string = Column(LargeBinary)

    def __init__(self, chat_id):
        self.chat_id = chat_id


gDriveCreds.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def set_credential(chat_id, credential_string):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        if not saved_cred:
            saved_cred = gDriveCreds(chat_id)

        saved_cred.credential_string = pickle.dumps(credential_string)

        SESSION.add(saved_cred)
        SESSION.commit()


def get_credential(chat_id):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        return (
            pickle.loads(saved_cred.credential_string)
            if saved_cred is not None
            else None
        )


def clear_credential(chat_id):
    with INSERTION_LOCK:
        if saved_cred := SESSION.query(gDriveCreds).get(chat_id):
            SESSION.delete(saved_cred)
            SESSION.commit()
