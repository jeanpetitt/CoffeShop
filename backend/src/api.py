import os
import re
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    #headers cors
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTION"
        )
        return response
    
    # db_drop_and_create_all()

    # ROUTES
    
    # get drinks with short information
    @app.route('/drinks')
    def get_drink():
        drinks = Drink.query.order_by(Drink.id).all()
        # get Drink it should contain only the drink.short()
        list_drink = [drink.short() for drink in drinks]
        print(list_drink)
        
        if len(list_drink) == 0:
            abort(404)
        return jsonify({
            'sucess': True,
            'drinks': list_drink,
            'total_drink': len(drinks)
        }), 200

    # get drink with more information
    @app.route('/drinks-detail')
    def get_drinks_detail():
        
        try:
            drinks = Drink.query.order_by(Drink.id).all()
            drinks = [drink.long() for drink in drinks]

            return jsonify({
                    'success': True,
                    'drinks': drinks,
                    'total_drinks': len(drinks)
                }), 200
    
        except:
            abort(404)


    # create a drink
    @app.route('/drinks', methods=['POST'])
    def post_drink():
        body = request.get_json()
        new_title = body.get('title', None)
        new_recipe = json.dumps(body['recipe'])
        # new_recipe = body.get('recipe')
        
        try:
            if 'title' and 'recipe' not in body:
                abort(422)
            
            drink = Drink(title=new_title, recipe=new_recipe)
            drink.insert()
            
            return jsonify({
                'success': True,
                'drink': drink.long(),
                'total_drinks': len(Drink.query.all())
                }), 200
        except:
            abort(422)


    # update the drink with permission required
    
    @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
    # require permission for update the drink
    @requires_auth('patch:drinks')
    def update_drink(drink_id, jwt):
        body = request.get_json()
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        try:
            if 'title' in body:
                drink.title = body.get('title', None)

            if 'recipe' in body:
                drink.recipe = json.dumps(body['recipe'])
            
            drink.update()
            drinks = [data.long() for data in drink ]
            
            return jsonify({
                'success': True,
                'drinks': drinks,
                'total_drinks': len(Drink.query.all())
            }), 200
            
        except:
            abort(400)

    # delete drink with permission required
    
    @app.route('/drinks/<int:drink_id>/delete', methods=['DELETE'])
    # permission required to delete a drink
    @requires_auth('delete:drinks')
    def delete_drink(drink_id, jwt):
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': drink_id,
                'total_drink': len(Drink.query.all())
            })
        except:
            abort(422)

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    #  implement error handlers 404 using the @app.errorhandler(error) decorator

    @app.errorhandler(404)
    def notFound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "ressource not found"
        }), 404
        
    # implement bad request
    @app.errorhandler(400)
    def badrequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    
    # implement AuthError
    @app.errorhandler(AuthError)
    def process_AuthError(error):
        response = jsonify(error.error)
        response.status_code = error.status_code

        return response

    return app
