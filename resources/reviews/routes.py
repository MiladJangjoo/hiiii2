from flask import request
from uuid import uuid4
from app import app
from db import reviews



@app.get('/review')
def get_review():
    return {'reviews': reviews}, 200

@app.get('/review/<review_id>')
def get_reviews(review_id):
    try:
        review = reviews[review_id]
        return review, 200
    except:
        return {'messege': 'review not found'}, 400


@app.post('/review')
def create_review():
    review_data = request.get_json()
    reviews[uuid4().hex] = review_data
    return review_data, 201

@app.put('/review/<review_id>')
def edit_review(review_id):
    review_data = request.get_json()
    if review_id in reviews:    
        review = reviews[review_id]
        review['body'] = review_data['body']
        return review, 200
    return {'messege': 'review not found'}, 400




@app.delete('/review/<review_id>')
def delete_review(review_id):
    try:
        deleted_review = reviews.pop(review_id)
        return {'messege': f'{deleted_review["body"]} deleted'}
    except:
        return {'messege': 'review not found'}, 400