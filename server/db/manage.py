from flask import current_app
from flask.cli import FlaskGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from server.db.data import page_files
from server.db.database import db
from server.db.models import Page

# cli = FlaskGroup(current_app)


# @cli.command("create_db")
def create_db():
    # db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command("seed_db")
def seed_db():
    engine = create_engine('postgresql+psycopg2://postgres:admin@localhost:5433/postgres')
    s = Session(bind=engine)
    pages = []
    for page in page_files:
        new_page = Page(name=page)
        pages.append(new_page)
    s.bulk_save_objects(pages)
    s.commit()


# if __name__ == "__main__":
#     cli()
