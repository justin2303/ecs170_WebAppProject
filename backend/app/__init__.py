from flask import Flask

# Create the Flask app instance
app = Flask(__name__)

# Import views to register the routes
from app import views