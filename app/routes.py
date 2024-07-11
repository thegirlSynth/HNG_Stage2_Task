#!/usr/bin/python3

"""
Endpoints
"""

from app import db
from helper import generate_uuid, error_response
from models import User, Organisation

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


my_app = Blueprint('main', __name__)

@my_app.route('/auth/register', methods=['POST'], strict_slashes=False)
def register():
    """
    Registers a user and creates a default organization
    """
    data = request.get_json()

    #Validate required fields
    required_fields = ['firstName', 'lastName', 'email', 'password']
    invalid_response = {"errors":[]}

    for field in required_fields:
        if field not in data:
            invalid_response["errors"].append({
                "field": field,
                "message": f"{field} is required"
                })

    if invalid_response["errors"]:
        return jsonify(invalid_response), 422

    #Check if email already exists
    if User.query.filter_by(email=data["email"]).first():
        return error_response("Email already registered", 422)

    try:
        user = User(
            userId=generate_uuid(),
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            phone=data.get('phone', ''),
        )

        org = Organisation(
            orgId=generate_uuid(),
            name=f"{user.firstName}'s Organisation",
            description="",
        )

        user.organisations.append(org)

        db.session.add(user)
        db.session.add(org)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return error_response(f"Registration unsuccessful: {str(e)}", 400)

    access_token = create_access_token(identity=user.userId)

    return jsonify(
        {'status': 'success',
         'message': 'Registration successful',
         'data': {
             'accessToken': access_token,
             'user': {
                 "userId": user.userId,
                 "firstName": user.firstName,
                 "lastName": user.lastName,
                 "email": user.email,
                 "phone": user.phone,
                },
            }
        }
    ), 201


@my_app.route('/auth/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Logs in a user
    """

    data = request.get_json()

    #Validate required fields
    required_fields = ['email', 'password']
    invalid_response = {"errors":[]}

    for field in required_fields:
        if field not in data:
            invalid_response["errors"].append({
                "field": field,
                "message": f"{field} is required"
                })

    if invalid_response["errors"]:
        return jsonify(invalid_response), 422

    #Check if user exists
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.userId)
        return jsonify(
            {
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': access_token,
                    'user': {
                        "userId": user.userId,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone": user.phone,
                    },
                }
            }
        ), 200

    return error_response("Authentication failed", 401)


@my_app.route('/api/users/<id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user(id):
    """
    Provides a user's record through a given user id,
    provided that the user Id is part of an organisation
    the logged in user belongs to/created
    """

    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(userId=current_user_id).first()

    # Check user permissions or ownership
    user = User.query.filter_by(userId=id).first()

    if not user:
        return error_response("User not found", 404)

    shared_organisations = set(current_user.organisations).intersection(user.organisations)

    if  user.userId != current_user_id or not shared_organisations: # Add Second condition here
        return error_response("Unauthorized", 401)

    return jsonify(
        {
            'status': 'success',
            'message': 'User data available',
            'data': {
                "userId": user.userId,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "email": user.email,
                "phone": user.phone,
            },
        }
    ), 200


@my_app.route('/api/organisations', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_orgs():
    """
    Gets all the organisations the user belongs to or created
    """
    current_user = get_jwt_identity()

    #Fetch organisations user belongs to or created
    user = User.query.filter_by(userId=current_user).first()
    orgs = user.organisations

    #Response payload
    org_list =[]
    for org in orgs:
        org_data = {
            "orgId": org.orgId,
            "name": org.name,
            "description": org.description,
        }
        org_list.append(org_data)

    response_data = {
        'status': 'success',
        "message": "Organisations retrieved",
        "data": { "organisations": org_list }
    }

    return jsonify(response_data), 200


@my_app.route('/api/organisations/<orgId>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_orgId(orgId):
    """
    Get the details of a specific organisation
    """
    user_id = get_jwt_identity()
    user = User.query.filter_by(userId=user_id).first()

    #Fetch organisation details
    organisation = Organisation.query.filter_by(orgId=orgId).first()
    if not organisation:
        return error_response("Organisation does not exist", 404)

    if user not in organisation.users:
        return error_response("Unauthorized", 403)

    #Prepare response payload
    response_data = {
        "status": "success",
        "message": "Organisation details retreived",
        "data": {
            "orgId": organisation.orgId,
            "name": organisation.name,
            "description": organisation.description,
        }
    }

    return jsonify(response_data), 200

@my_app.route('/api/organisations', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_orgs():
    """
    Creates a new organisation
    """
    current_user= get_jwt_identity()
    user = User.query.filter_by(userId=current_user).first()

    data = request.get_json()

    #Validate required fields
    if "name" not in data:
        return jsonify(
            {"errors":
             [{
                 "field": "name",
                 "message": "name is required",
                 }]
            }), 422

    try:
        new_org = Organisation(
            orgId=generate_uuid(),
            name=data['name'],
            description=data.get('description', 'Great organisation')
        )

        user.organisations.append(new_org) #Review this

        db.session.add(new_org)
        db.session.commit()

    except:
        db.session.rollback()
        return error_response("Client error", 400)

    #Response payload
    response_data = {
        "status": "success",
        "message": "Organisation created successfully",
        "data": {
            "orgId": new_org.orgId,
            "name": new_org.name,
            "description": new_org.description
        }
    }

    return jsonify(response_data), 201

@my_app.route('/api/organisations/<orgId>/users', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_user_to_org(orgId):
    """
    Adds a user to a specific organisation
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(userId=current_user_id).first()

    data = request.get_json()
    user_id =data.get('userId')

    #Validate required fields
    if not user_id:
        return jsonify(
            {"errors":
             [{
                 "field": "userId",
                 "message": "userId is required",
                 }]
            }), 422


    organisation = Organisation.query.filter_by(orgId=orgId).first()
    if not organisation:
        return error_response("Organization not found", 404)

    user = User.query.filter_by(userId=user_id).first()
    if not user:
        return error_response("User does not exist", 404)

    if user in organisation.users:
        return error_response("User already belongs to this organization", 400)

    if current_user not in organisation.users:
        return error_response("Unauthorized", 403)

    #Add user to organisation
    try:
        organisation.users.append(user)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 400)

    #Response payload
    response_data = {
        "status": "success",
        "message": "User added to organisation successfully",
    }

    return jsonify(response_data), 200


