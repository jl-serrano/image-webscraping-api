from flask_restful import Api
from app import app
from api.v1.image_scraper import Scraping

api = Api(app)

# routes
api.add_resource(Scraping, '/api/v1/scraping')