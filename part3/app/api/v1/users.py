#!/usr/bin/python3
"""User API endpoints with JWT protection examples"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

# =======================
# Models
# =======================

# Model for CREATE (POST) - all required, including password
user_create_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Model for UPDATE (PUT) - all optional (partial update)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user')
})

# =======================
# Routes
# =======================

@api.route('/')
class UserList(Resource):
    @jwt_required()  # Protected endpoint - requires valid JWT
    @api.expect(user_create_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user (Admin only)"""
        # Check if user is admin
        current_user = get_jwt()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        # Check email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            # Return user info without password
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()  # Protected endpoint - requires valid JWT
    @api.response(200, 'List of users retrieved successfully')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def get(self):
        """Get list of users (Protected - requires JWT)"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        
        users = facade.get_all_users()
        # Exclude password from response
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()  # Protected endpoint - requires valid JWT
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def get(self, user_id):
        """Get user by ID (Protected - requires JWT)"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Exclude password from response
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()  # Protected endpoint - requires valid JWT
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """Update user by ID (Protected - requires JWT)"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        
        # Users can only update their own profile, unless they're admin
        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        user_data = api.payload

        # Non-admin users cannot modify email or password
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400

        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Admin trying to change email - check uniqueness
        if is_admin and 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            # Handle password hashing if admin is updating password
            if is_admin and 'password' in user_data:
                # We need to hash the password before updating
                user.hash_password(user_data['password'])
                del user_data['password']  # Remove from user_data as it's already set
            
            # Handle email update if admin is updating email
            if is_admin and 'email' in user_data:
                user.email = user_data['email']
                del user_data['email']  # Remove from user_data as it's already set

            # Update remaining fields
            facade.update_user(user_id, user_data)

            updated_user = facade.get_user(user_id)
            # Exclude password from response
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400