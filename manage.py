from flask import current_app
from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash

from server.db.data import page_files
from server.db.database import db
from server.db.imports import import_classifications
from server.db.models import Page, User
import click

cli = FlaskGroup(current_app)


@cli.command("create_db")
def create_db():
    print('creating DB')
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    print('seed_db')
    pages = []
    for page in page_files:
        new_page = Page(name=page)
        pages.append(new_page)
    db.session.bulk_save_objects(pages)
    db.session.commit()


@cli.command("import_data")
def import_data():
    print('import')
    path = current_app.config['CLASSIFICATION_PATH']
    import_classifications(path)


@cli.command("import_data")
def import_data():
    print('import')
    path = current_app.config['CLASSIFICATION_PATH']
    import_classifications(path)


@cli.command("create_user")
@click.argument('email')
def create_user(email):
    print('new user', email)
    hashed_password = generate_password_hash('password', method='sha256')
    new_user = User(
        email=email,
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()


if __name__ == "__main__":
    print('cli')
    cli()
