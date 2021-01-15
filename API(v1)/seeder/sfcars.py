import json
from dbmodels.sfcars import Sfcars
from dbmodels.initdb import db

def sfcars_seeder(classesloc, image_idx_loc):
    """
    :param db : SQLAlchemy DB
    :param classesloc: PATH of json file with class names
    :param image_idx_loc: PATH of json file with image index
    :return: None
    """
    with open(classesloc) as f:
        classes = json.load(f)
    with open(image_idx_loc) as f:
        car_images = json.load(f)
    for car in classes['a']:
        c = Sfcars(car_name=car, car_image=car_images[car])
        db.session.add(c)
    db.session.commit()

