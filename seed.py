"""
Populate twitter database with fake data using the SQLAlchemy ORM.
"""
import datetime
import random
import string
import hashlib
import secrets
import requests
import random
from faker import Faker
from tube_tv.src.models import User, Film, Actor, Genre, purchases, film_actors, film_genres, db
from tube_tv.src import create_app


def fetch_api(api):
    try:
        data = requests.get(api)
    except:
        print('was not able to fetch the data')
        return {}
    else:
        return data.json()['contents']


fetched_data = fetch_api('https://tubitv.com/oz/containers')
arr = [fetched_data[el] for el in fetched_data]


movies_list = list(map(lambda x: {
    "title": x['title'],
    'release_year': x['year'],
    'length': random.randint(60, 151),
    'rating': random.choice(['G', 'PG', None, 'PG-13', 'R', 'NC-17']),
    'price': random.choice([0.0, 0.99, 4.99, 19.99, 6.99, 14.99, 11.99])
}, arr))

for el in movies_list:
    print(el)

USER_COUNT = 50
FILM_COUNT = len(movies_list)
ACTOR_COUNT = 100


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

    # TODO: fake data fo 'users' table
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

    # TODO: fake data for 'films' table
    last_film = None # save last film
    for el in movies_list:
        last_film = Film(
            title=el['title'],
            release_year=el['release_year'],
            length=el['length'],
            rating=el['rating'],
            price=el['price'],
            date_added=str(fake.date())
        )
        # insert film
        db.session.add(last_film)
    db.session.commit()

    # TODO: fake data for 'actors' table
    last_actor = None  # save last actor
    for _ in range(ACTOR_COUNT):
        last_actor = Actor(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        # insert actor
        db.session.add(last_actor)

    db.session.commit()

    # TODO: fake data for 'genres' table
    genre_list = ["Comedy", "Action", "Cartoon", "Horror", "History",
                  "Thriller", "Drama","Mystery", "Fantasy", "Western"]
    last_genre = None # save last genre
    for g in genre_list:
        last_genre = Genre(
            genre=g
        )
        # insert genre
        db.session.add(last_genre)
    db.session.commit()


# run script
main()
























