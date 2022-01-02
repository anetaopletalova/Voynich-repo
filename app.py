from flask import Flask
from flask_cors import CORS

from server.db.database import db
from manage import import_data, seed_db
from server.routes.home import home_page
from server.routes.auth import auth
from server.routes.note import note_route
from server.routes.page import page_route


app = Flask(__name__)
app.config.from_object("config.Config")

app.register_blueprint(home_page)
app.register_blueprint(auth)
app.register_blueprint(page_route)
app.register_blueprint(note_route)

CORS(app)


db.init_app(app)
with app.app_context():
    # db.drop_all()
    db.create_all()
    # seed_db()
    # import_data()
    db.session.commit()

    pass

if __name__ == '__main__':
    app.run()
