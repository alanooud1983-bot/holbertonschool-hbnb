from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# ------------------ Models ------------------

# Input validation model (CREATE) - user_id removed, will be set from JWT
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Input validation model (UPDATE) - only fields allowed to update
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)')
})

# ------------------ /api/v1/reviews/ ------------------
@api.route('/')
class ReviewList(Resource):
    @jwt_required()  # Protected endpoint - requires valid JWT
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def post(self):
        """Register a new review (Protected - requires JWT)"""
        try:
            # Get current user from JWT token
            current_user = get_jwt_identity()
            
            review_data = request.json or {}
            place_id = review_data.get('place_id')
            
            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            
            # Check that the user is not the owner of the place
            if place.owner_id == current_user:
                return {"error": "You cannot review your own place"}, 400
            
            # Check if the user has already reviewed this place
            existing_reviews = facade.get_reviews_by_place(place_id)
            for review in existing_reviews:
                review_user_id = review.user.id if getattr(review, "user", None) else getattr(review, "user_id", None)
                if review_user_id == current_user:
                    return {"error": "You have already reviewed this place"}, 400
            
            # Set user_id to the authenticated user
            review_data['user_id'] = current_user
            
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews (Public)"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

# ------------------ /api/v1/reviews/<review_id> ------------------
@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (Public)"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @jwt_required()  # Protected endpoint - requires valid JWT
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review (Protected - requires JWT)"""
        try:
            # Get current user from JWT token
            current_user_id = get_jwt_identity()
            current_user = get_jwt()
            is_admin = current_user.get('is_admin', False)
            
            # Get the review to check ownership
            review = facade.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404
            
            # Check if the user is the owner of the review (admins can bypass)
            review_user_id = review.user.id if getattr(review, "user", None) else getattr(review, "user_id", None)
            if not is_admin and review_user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403
            
            updated_review = facade.update_review(review_id, request.json)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()  # Protected endpoint - requires valid JWT
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review (Protected - requires JWT)"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        
        # Get the review to check ownership
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        
        # Check if the user is the owner of the review (admins can bypass)
        review_user_id = review.user.id if getattr(review, "user", None) else getattr(review, "user_id", None)
        if not is_admin and review_user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200