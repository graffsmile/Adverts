import pydantic
from flask import Flask, jsonify, request, Response
from flask.views import MethodView
from pydantic import ValidationError
from requests import HTTPError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from models import engine, User, Adverts
from schema import Adv as AdvValidator, User as UserValidator

Session = sessionmaker(engine)

app = Flask("my_app")

class UserView(MethodView):
    def get(self, id: int):
        user_object: User = request.session.get(User, {'id': id})

        if not user_object:
            return jsonify({'status': 'error', 'user': 'object not found'})

        user_object_dict = user_object.__dict__
        user_object_dict.pop('_sa_instance_state', None)
        return jsonify({'status': 'ok', 'user': user_object_dict})


    def post(self):
        params = request.json

        try:
            user = UserValidator(**params)
            user_object = user.model_dump()
            request.session.add(User(**user_object))
            request.session.commit()


        except ValidationError:
            return jsonify({'status': 'error', 'message': 'validation error'})

        return jsonify({'status': 'ok', 'message': user.model_dump()})




class AdvView(MethodView):
    def get(self, Adv_id: int):
        adv_object: Adverts = request.session.get(Adverts, {'id': Adv_id})

        if not adv_object:
            return jsonify({'status': 'error', 'advert': 'object not found'})

        adv_object_dict = adv_object.__dict__
        adv_object_dict.pop('_sa_instance_state', None)
        return jsonify({'status': 'ok', 'advert': adv_object_dict})

    def post(self):
        params = request.json
        try:
            advert = AdvValidator(**params)
            adv_object = advert.model_dump()
            request.session.add(Adverts(**adv_object))
            request.session.commit()
        except ValidationError:
            return jsonify({'status': 'error', 'message': 'validation error'})

        return jsonify({'status': 'ok', 'message': advert.model_dump()})

    def patch(self, Adv_id):
        json_data = request.json
        with Session() as session:
            adv = session.query(Adverts).filter(Adverts.id == Adv_id).first()
            for field, value in json_data.items():
                setattr(adv, field, value)
                try:
                    session.commit()
                except IntegrityError as error:
                    raise HTTPError(409, error)

                return jsonify({
                    'status': 'success',
                    'id': adv.id,
                })




    def delete(self, Adv_id):
        try:
            with Session() as session:
                advert = session.query(Adverts).filter(Adverts.id == Adv_id).first()
                session.delete(advert)
                session.commit()
                return jsonify(f'advert {Adv_id}: deleted')
        except pydantic.ValidationError as error:
            raise HTTPError(400, error)



@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(http_response: Response):
    request.session.close()
    return http_response

app.add_url_rule('/adverts/',
                 view_func=AdvView.as_view('Advert'),
                 methods=['POST']
                 )

app.add_url_rule('/user/',
                 view_func=UserView.as_view('User'),
                 methods=['POST']
                 )

app.add_url_rule('/adverts/<int:Adv_id>',
                 view_func=AdvView.as_view('adverts'),
                 methods=['GET', 'PATCH', 'DELETE']
                 )

app.add_url_rule('/user/<int:id>',
                 view_func=UserView.as_view('users'),
                 methods=['GET']
                 )

if __name__ == '__main__':

    app.run(
        debug=True,
    )