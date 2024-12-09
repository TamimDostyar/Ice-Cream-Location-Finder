from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class IceCream(db.Model):
    __tablename__ = "icecream"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<IceCream {self.name}>"
