from crypt import methods
import os
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
    

    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this funciton will add one
    '''
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
        })

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
                })
    
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
            print('ma famille "bonjour": "[{}]" ')
            
            drink = Drink(title=new_title, recipe=new_recipe)
            drink.insert()
            
            return jsonify({
                'success': True,
                'created': drink.id,
                'total_drinks': len(Drink.query.all())
                })
        except:
            abort(422)
        
        


    '''
    @TODO implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''


    '''
    @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''


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

    return app
