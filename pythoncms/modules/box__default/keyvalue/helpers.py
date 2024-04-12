from .models import KeyValue
from init import db

def set_value(key, value):
    keyvalue = KeyValue.query.filter(KeyValue.key == key).first()
    if keyvalue:
        keyvalue.value = value
        keyvalue.update()
    else:
        s = KeyValue(key=key,value=value)
        db.session.add(s)
        db.session.commit()


def get_value(key):
    """
    Used as key-value lookup from KeyValue table

    Parameters
    ----------
    name: str
        name of key

    Returns
    -------
    str
        value of key
    """
    s = KeyValue.query.filter(KeyValue.key == key).first()

    if s:
        return s.value
    else:
        return ''
