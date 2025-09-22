from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    reviews = db.relationship("Review", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    reviews = db.relationship("Review", back_populates="game")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    game = db.relationship("Game", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    @validates("score")
    def validate_score(self, key, value):
        if value < 0 or value > 10:
            raise ValueError("Score must be between 0 and 10")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "score": self.score,
            "comment": self.comment,
            "game_id": self.game_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat()
        }
