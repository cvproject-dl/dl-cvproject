from flask_restful import Resource, reqparse
from pytorch_helper.constants import SFCARS_PARAM,INDCARS_PARAM
from models.sfcars import Sfcars
from models.indiacars import Indiacars


class Cars(Resource):
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('page', type=int)
        parse.add_argument('model', required=True, help=f"Model cannot be blank.{SFCARS_PARAM}/{INDCARS_PARAM}")
        parse.add_argument('search')
        args = parse.parse_args()
        page = args['page']
        search_term = args['search']
        model_name = args['model']
        try:
            if model_name.strip() == SFCARS_PARAM:
                res = Sfcars.get_items(page=page) if search_term is None else Sfcars.search_by_name(
                    search_term=search_term,
                    page=page)
            elif model_name.strip() == INDCARS_PARAM:
                res = Indiacars.get_items(page=page) if search_term is None else Indiacars.search_by_name(
                    search_term=search_term,
                    page=page)
            else:
                return {"message": {'error': "Invalid Model Name", 'status': 404}}, 404
            return {'cars': res, 'status': 200}, 200
        except Exception as e:
            return {"message": {'error': f"Internal Server Error {str(e)}", 'status': 500}}, 500


