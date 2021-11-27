"""
Populate twitter database with fake data using the SQLAlchemy ORM.
"""
import datetime
import random
import string
import hashlib
import secrets
from faker import Faker
from tube_tv.src.models import User, Film, Actor, Genre, purchases, film_actors, film_genres, db
from tube_tv.src import create_app

USER_COUNT = 50


def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    )
    salt = secrets.token_hex(16)
    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


# TODO: Delete all data from tables
def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(purchases.delete())
    db.session.execute(film_actors.delete())
    db.session.execute(film_genres.delete())
    User.query.delete()
    Film.query.delete()
    Actor.query.delete()
    Genre.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    last_user = None  # save last user
    for _ in range(USER_COUNT):
        last_user = User(
            username=fake.unique.first_name().lower() + str(random.randint(1, 150)),
            password=random_passhash(),
            email=fake.unique.first_name().lower() + '@'
                  + random.choice(['@yahoo', 'gmail', 'mail', 'hotmail']) + '.com',
            created_at=str(fake.date())
        )
        db.session.add(last_user)

    # insert users
    db.session.commit()


# run script
main()
