import json
from dbmodels.indiacars import Indiacars
from dbmodels.initdb import db

def indiacars_seeder(classesloc):
    """
    :param db : SQLAlchemy DB
    :param classesloc:PATH of json file with class names
    :return:
    """
    with open(classesloc) as f:
        classes = json.load(f)
    for car in classes['b']:
        c = Indiacars(car_name=car, car_image=car.lower().replace(" ", "_") + '.jpg')
        db.session.add(c)
    db.session.commit()
