from app import db
from datetime import datetime


class ReviewModel(db.Model):

    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.String, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __repr__(self):
        return f'<review: {self.body}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()