from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from pytorch_helper.resnet34 import load_model, predict
from pytorch_helper.constants import SF_CARS, INDIA_CARS, INDCARS_PARAM, SFCARS_PARAM
import os


class Predict(Resource):
    ALLOWED_EXTENTIONS = {'jpeg', 'jpg', 'png'}

    def __allowedfile(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Predict.ALLOWED_EXTENTIONS

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('image', type=FileStorage, location='files', required=True)
        parse.add_argument('model', required=True, choices=(SFCARS_PARAM, INDCARS_PARAM),
                           help=f"Model should be '{SFCARS_PARAM}' or '{INDCARS_PARAM}'")
        args = parse.parse_args()
        image_file = args['image']
        model_name = args['model']
        print(image_file.filename)
        if image_file and self.__allowedfile(image_file.filename):
            try:
                filename = secure_filename(image_file.filename)
                loc = os.path.join('uploads', filename)
                image_file.save(loc)
                if model_name.strip() == SFCARS_PARAM:
                    model = load_model(SF_CARS, chkpt_model=SFCARS_PARAM)
                    res = predict(model=model, fileloc=loc, chkpt_model=SFCARS_PARAM)
                elif model_name.strip() == INDCARS_PARAM:
                    model = load_model(INDIA_CARS, chkpt_model=INDCARS_PARAM)
                    res = predict(model=model, fileloc=loc, chkpt_model=INDCARS_PARAM)
                else:
                    os.remove(loc)
                    return {"message": {'error': "Invalid Model Name", 'status': 404}}, 404
                os.remove(loc)
                return {'predictions': res, 'status': 200}, 200
            except Exception as e:
                return {"message": {'error': f"Internal Server Error {str(e)}", 'status': 500}}, 500

        else:
            return {"message": {'error': "Invalid Filename", 'status': 404}}, 404
