from distutils.log import debug
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
	from api import *
	app.run(host="0.0.0.0", port=23450, use_reloader=True, debug=True)