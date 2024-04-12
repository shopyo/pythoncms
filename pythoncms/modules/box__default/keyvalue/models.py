from init import db


class KeyValue(db.Model):
    __tablename__ = "keyvalue"
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(100), unique=True)
    value = db.Column(db.String(100))

    def add(self):
        db.session.add(self)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
