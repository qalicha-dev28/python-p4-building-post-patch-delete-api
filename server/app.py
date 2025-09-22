from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, User, Game, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()

    try:
        review = Review(
            score=data['score'],
            comment=data.get('comment'),
            game_id=data['game_id'],
            user_id=data['user_id']
        )
        db.session.add(review)
        db.session.commit()
        return make_response(review.to_dict(), 201)
    except Exception as e:
        return make_response({"error": str(e)}, 400)


@app.route('/reviews/<int:id>', methods=['PATCH'])
def update_review(id):
    review = Review.query.get_or_404(id)
    data = request.get_json()

    if "score" in data:
        review.score = data["score"]
    if "comment" in data:
        review.comment = data["comment"]

    db.session.commit()
    return make_response(review.to_dict(), 200)


@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return make_response({}, 204)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
