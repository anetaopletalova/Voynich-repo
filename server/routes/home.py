from flask import Blueprint

home_page = Blueprint('home_page', __name__)


@home_page.route('/')
def hello_world():
    return 'Hello World!'
