from .initdb import db


class Indiacars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(80), unique=True, nullable=False)
    car_image = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f'<Indiacars {self.car_name}>'

    @staticmethod
    def __item_to_json(item):
        host = "https://carimage.netlify.app"
        resp = dict()
        resp['id'] = item.id
        resp['name'] = item.car_name
        resp['image'] = f"{host}/{item.car_image}"
        return resp

    @classmethod
    def get_items(cls, page):
        if page is None:
            page = 1
        all_items = cls.query.all()
        results = list()
        start = (page - 1) * 10
        last_idx = len(all_items) - 1
        if last_idx < start:
            start = last_idx - 10
        total = 0
        for item in all_items[start:]:
            if total >= 10:
                break
            results.append(cls.__item_to_json(item))
            total += 1
        return results

    @classmethod
    def get_item_by_id(cls, idno):
        item = cls.query.filter_by(id=idno).first()
        return cls.__item_to_json(item)
