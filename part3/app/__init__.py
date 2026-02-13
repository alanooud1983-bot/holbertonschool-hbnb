from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from app.extensions import db, bcrypt, jwt
from flask_cors import CORS 

migrate = Migrate()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],  # Add your frontend URLs
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate
    
    # Import namespaces INSIDE create_app to avoid circular imports
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns
    
    api = Api(app, version="1.0", title="HBnB API", description="HBnB Application API")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(auth_ns, path="/api/v1")
    
    return app
