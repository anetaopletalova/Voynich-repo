from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from server.db.database import db
from server.routes.home import home_page
from server.routes.auth_routes import auth
app = Flask(__name__)
app.config.from_object("config.Config")

app.register_blueprint(home_page)
app.register_blueprint(auth)


# import models to create the tables!
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    app.run()
