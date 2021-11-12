from flask import Flask
from server.db.database import db
from server.db.manage import seed_db
from server.routes.home import home_page
from server.routes.auth_routes import auth
from server.routes.page import page_route

app = Flask(__name__)
app.config.from_object("config.Config")

app.register_blueprint(home_page)
app.register_blueprint(auth)
app.register_blueprint(page_route)

db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    app.run()
