"""
To insert car details to the database.
Delete this package before deploying.

"""

from flask import Flask
from models.initdb import db
from seeder import sfcars_seeder, indiacars_seeder


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize database

db.init_app(app)

with app.app_context():
    db.create_all()
    sfcars_seeder(classesloc='class_names/classes.json', image_idx_loc='class_names/car_images.json')
    indiacars_seeder(classesloc='class_names/classes.json')
