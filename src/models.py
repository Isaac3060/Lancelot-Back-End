from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Business(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     business_name = db.Column(db.String(80), unique=False, nullable=False)
     address = db.Column(db.String(120), unique=False, nullable=False)
     phone_number = db.Column(db.String(120), unique=False, nullable=False)
     email = db.Column(db.String(120), unique=True, nullable=False)
     password = db.Column(db.String(120), unique=False, nullable=False)#
     visits = db.relationship("Visit")

     def __repr__(self):
        return '<Business %r>' % self.business_name

     def serialize(self):
        return {
            "id": self.id,
            "business_name": self.business_name,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "visitors": list(map(lambda x: x.serialize(), self.visitors))
        }

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    phone_number = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    visits = db.relationship("Visit")

    def __repr__(self):
        return '<Visitor %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "visit": list(map(lambda x: x.serialize(), self.visits))
        }

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120), unique=True, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey(Business.id))
    visitor_id = db.Column(db.Integer, db.ForeignKey(Visitor.id),nullable=False)
    entry_date = db.Column(db.DateTime(120), unique=False, nullable=False)
    has_fever = db.Column(db.Boolean(), unique=False, nullable=False, default=False)#
    has_covid = db.Column(db.Boolean (), unique=False, nullable=False , default=False)#
    
    def __repr__(self):
        return '<Visit %r>' % self.image

    def serialize(self):
        return {
            "id": self.id,
            "image": self.image,
            "entry_date": self.entry_date,
            "has_fever": self.has_fever,
            "has_covid": self.has_covid  
        }