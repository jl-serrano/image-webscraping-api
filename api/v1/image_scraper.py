from enum import Enum
import os
from flask_restful import Resource, reqparse
from webscraper.bs_scraper import main as scraper
from urllib.parse import urlparse

parser = reqparse.RequestParser()
parser.add_argument('image_url', required=True, help="image_url cannot be blank.")
parser.add_argument('image_url_target')

State = Enum('State', 'ALL_IMAGES IMAGES_FROM_TARGET')


class Scraping(Resource):
    def __pathname(self, url):
        #Make the website's hostname as folder pathname
        args = parser.parse_args()
        parse_url = urlparse(url).netloc
        new_url = '.'.join(parse_url.split('.')[-2:])
        pathname = new_url[:-4]
        return pathname

    def post(self):
        os.chdir("downloads")

        args = parser.parse_args()
        return scraper(
            args['image_url'], 
            self.__pathname(args['image_url']),          
            State.ALL_IMAGES.name if args['image_url_target'] is None else State.IMAGES_FROM_TARGET.name,
            args['image_url_target'] if args['image_url_target'] is not None else ''
        )
        