from flask import request
from uuid import uuid4

from app import app
from db import users, reviews


@app.get('/user')
def get_users():
    return {'users': users}, 200

@app.get('/user/<user_id>')
def get_user(user_id):
    try:
        user = users[user_id]
        return user, 200
    except:
        return {'messege': 'user not found'}, 400



@app.post('/user')   # sending us some data thats why we need request
def create_user():
    user_data = request.get_json()
    users[uuid4().hex] = user_data
    return user_data, 201



@app.put('/user/<user_id>')
def update_user(user_id):
    user_data = request.get_json()
    try:
        user = users[user_id]
        user['username'] = user_data['username']
        return user, 200
    except:
        return {'messege': 'user not found'}, 400



@app.delete('/user')
def delete_user():
    user_data = request.get_json()
    for i,user in enumerate(users):
        if user['username'] == user_data['username']:
            users.pop(i)
    return {'messege' : f'{user_data["username"]} deleted'}, 202

@app.get('/user/<user_id>/review')
def get_user_review(user_id):
    if user_id not in users:
        return {'messege': 'user not found'}, 400
    user_reviews = [review for review in reviews.values() if review['user_id'] == user_id]
    return user_reviews, 200