from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace("places", description="Place operations")

# ==================== MODELS ====================

amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(description="Amenity ID"),
        "name": fields.String(description="Name of the amenity"),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name of the owner"),
        "last_name": fields.String(description="Last name of the owner"),
        "email": fields.String(description="Email of the owner"),
    },
)

review_model = api.model(
    "PlaceReview",
    {
        "id": fields.String(description="Review ID"),
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(required=True, description="Rating of the place (1-5)"),
        "user_id": fields.String(description="ID of the user"),
    },
)

place_create_model = api.model(
    "PlaceCreate",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "owner_id": fields.String(required=True, description="ID of the owner"),
        "amenities": fields.List(fields.String, description="List of amenity IDs"),
    },
)

place_update_model = api.model(
    "PlaceUpdate",
    {
        "title": fields.String(description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(description="Price per night"),
        "latitude": fields.Float(description="Latitude of the place"),
        "longitude": fields.Float(description="Longitude of the place"),
        "owner_id": fields.String(description="ID of the owner"),
        "amenities": fields.List(fields.String, description="List of amenity IDs"),
    },
)

place_model = api.model(
    "Place",
    {
        "id": fields.String(description="Place ID"),
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "owner_id": fields.String(required=True, description="ID of the owner"),
        "owner": fields.Nested(user_model, description="Owner of the place"),
        "amenities": fields.List(
            fields.Nested(amenity_model), description="List of amenities"
        ),
        "reviews": fields.List(
            fields.Nested(review_model), description="List of reviews"
        ),
    },
)


# ==================== HELPER FUNCTIONS ====================

def serialize_place(
    place, include_owner=True, include_amenities=True, include_reviews=False
):
    data = {
        "id": place.id,
        "title": place.title,
        "description": getattr(place, "description", None),
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": place.owner_id,
    }

    if include_owner and getattr(place, "owner", None):
        data["owner"] = {
            "id": place.owner.id,
            "first_name": place.owner.first_name,
            "last_name": place.owner.last_name,
            "email": place.owner.email,
        }

    if include_amenities:
        data["amenities"] = [
            {"id": a.id, "name": a.name} for a in getattr(place, "amenities", [])
        ]

    if include_reviews:
        reviews = facade.get_reviews_by_place(place.id)
        data["reviews"] = [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": (
                    r.user.id
                    if getattr(r, "user", None)
                    else getattr(r, "user_id", None)
                ),
            }
            for r in (reviews or [])
        ]

    return data


# ==================== ROUTES ====================

@api.route("/")
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized - Invalid or missing token")
    def post(self):
        """Register a new place (Protected - requires JWT)"""
        try:
            current_user = get_jwt_identity()

            payload = api.payload or {}
            payload["owner_id"] = current_user

            place = facade.create_place(payload)
            return (
                serialize_place(
                    place,
                    include_owner=False,
                    include_amenities=False,
                    include_reviews=False,
                ),
                201,
            )
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Get all places (Public)"""
        places = facade.get_all_places()
        return [
            serialize_place(
                p, include_owner=False, include_amenities=False, include_reviews=False
            )
            for p in places
        ], 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID (Public)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return (
            serialize_place(
                place, include_owner=True, include_amenities=True, include_reviews=True
            ),
            200,
        )

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized - Invalid or missing token")
    @api.response(403, "Unauthorized action")
    def put(self, place_id):
        """Update a place's information (Protected - requires JWT)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = get_jwt()
            is_admin = current_user.get('is_admin', False)

            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            # Check ownership - admins can bypass this check
            if not is_admin and place.owner_id != current_user_id:
                return {"error": "Unauthorized action"}, 403

            payload = api.payload or {}
            if "owner_id" in payload:
                del payload["owner_id"]

            updated = facade.update_place(place_id, payload)
            return (
                serialize_place(
                    updated,
                    include_owner=True,
                    include_amenities=True,
                    include_reviews=True,
                ),
                200,
            )
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place (Public)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id if getattr(r, "user", None) else getattr(r, "user_id", None),
                "place_id": place_id
            }
            for r in (reviews or [])
        ], 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def post(self, place_id):
        """Create a review for a place (Protected - requires JWT)"""
        try:
            # Verify place exists
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            current_user_id = get_jwt_identity()
            
            # Get review data
            data = api.payload or {}
            data['place_id'] = place_id
            data['user_id'] = current_user_id
            
            # Validate rating
            rating = data.get('rating')
            if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
                return {"error": "Rating must be an integer between 1 and 5"}, 400
            
            # Validate text
            if not data.get('text') or not data['text'].strip():
                return {"error": "Review text is required"}, 400

            # Create review
            review = facade.create_review(data)
            
            return {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": current_user_id,
                "place_id": place_id,
                "message": "Review created successfully"
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/<place_id>/amenities/<amenity_id>')
class PlaceAmenity(Resource):
    @jwt_required()
    @api.response(200, 'Amenity added to place successfully')
    @api.response(404, 'Place or amenity not found')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    @api.response(403, 'Unauthorized action')
    def post(self, place_id, amenity_id):
        """Add an amenity to a place (Protected - requires JWT)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = get_jwt()
            is_admin = current_user.get('is_admin', False)

            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            # Check ownership - admins can bypass this check
            if not is_admin and place.owner_id != current_user_id:
                return {"error": "Unauthorized action"}, 403

            # Add amenity to place
            updated_place = facade.add_amenity_to_place(place_id, amenity_id)
            
            return {
                "message": "Amenity added successfully",
                "place": serialize_place(
                    updated_place,
                    include_owner=True,
                    include_amenities=True,
                    include_reviews=False
                )
            }, 200

        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @api.response(200, 'Amenity removed from place successfully')
    @api.response(404, 'Place or amenity not found')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    @api.response(403, 'Unauthorized action')
    def delete(self, place_id, amenity_id):
        """Remove an amenity from a place (Protected - requires JWT)"""
        try:
            current_user_id = get_jwt_identity()
            current_user = get_jwt()
            is_admin = current_user.get('is_admin', False)

            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            # Check ownership - admins can bypass this check
            if not is_admin and place.owner_id != current_user_id:
                return {"error": "Unauthorized action"}, 403

            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": "Amenity not found"}, 404

            # Remove amenity from place
            if amenity in place.amenities:
                place.amenities.remove(amenity)
                facade.update_place(place_id, {})  # Trigger update to save changes
                
            return {
                "message": "Amenity removed successfully"
            }, 200

        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": str(e)}, 400