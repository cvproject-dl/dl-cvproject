from flask_restful import Resource, reqparse
from pytorch_helper.constants import SFCARS_PARAM, INDCARS_PARAM
from models import Sfcars, Indiacars


class Cars(Resource):
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('page', type=int)
        parse.add_argument('model', required=True, choices=(SFCARS_PARAM, INDCARS_PARAM),
                           help=f"Model should be '{SFCARS_PARAM}' or '{INDCARS_PARAM}'")
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
            if len(res) > 0:
                val = {'cars': res, 'status': 200, 'invalidPage': False}, 200
            else:
                val = {'cars': res, 'status': 400, 'invalidPage': True}, 400
            return val
        except Exception as e:
            return {"message": {'error': f"Internal Server Error {str(e)}", 'status': 500}}, 500
