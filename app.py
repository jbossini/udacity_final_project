import os
from flask import Flask, request, jsonify, abort
from models import setup_db, db, Comic, Series, Editorial
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import exc


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate = Migrate(app, db)
    """ MEthods concerning comics"""
    @app.route('/comics')
    def get_comics():
        comics = [comic.format() for comic in Comic.query.all()]
        print(comics)
        return jsonify({'success': True, 'comics': comics, 'total_comics': len(comics)})

    @app.route('/comics/<int:id>')
    def get_comic_detail(id):
        comic = Comic.query.filter(Comic.id == id).one_or_none()
        if comic is None:
            abort(404)
        return jsonify({
            'success': True,
            'comic': comic.format()
        })

    @app.route('/comics', methods=['POST'])
    def create_comic():
        return "Success=True y el id del comic insertado si todo ha ido bien"

    @app.route('/comics/<int:id>', methods=['DELETE'])
    def delete_comic(id):
        return "Borra un comic"

    @app.route('/comics/<int:id>', methods=['PATCH'])
    def update_comic(id):
        return "actualiza el comic"
    """Methods concerning the series"""
    @app.route('/series')
    def get_series():
        series = [serie.format() for serie in Series.query.all()]
        return jsonify({
            'success': True,
            'series': series,
            'total_series': len(series)})

    @app.route('/series/<int:id>')
    def get_series_detail(id):
        serie = Series.query.filter(Series.id == id).one_or_none()
        if serie is None:
            abort(404)
        return jsonify({
            'success': True,
            'serie': serie.format()
        })

    @app.route('/series', methods=['POST'])
    def create_series():
        data = request.get_json()
        name = data.get('name', None)
        editorial_id = data.get('editorial_id', None)
        editorial = Editorial.query.filter(
            Editorial.id == editorial_id).one_or_none()
        """We must check if the editorial exists if not we abort with error PRecondition failed"""
        if editorial is None:
            abort(412)

        try:
            serie = Series(name, editorial_id)
            serie.insert()
            return jsonify({
                'success': True,
                'id_serie': serie.id
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    @app.route('/series/<int:id>', methods=['DELETE'])
    def delete_series(id):
        serie = Series.query.filter(Series.id == id).one_or_none()
        if serie is None:
            abort(404)
        try:
            serie.delete()
            return jsonify({
                'success': True,
                'id_serie': id
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    @app.route('/series/<int:id>', methods=['PATCH'])
    def update_series(id):
        serie = Series.query.filter(Series.id == id).one_or_none()
        if serie is None:
            abort(404)
        data = request.get_json()
        serie.name = data.get('name', serie.name)
        serie.editorial_id = data.get('editorial_id', serie.editorial_id)
        try:
           serie.update()
           return jsonify({
                'success': True,
                'serie': serie.format()
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    """ Methods concerning the editorials"""
    @app.route('/editorials')
    def get_editorials():
        editorials = [editorial.format()
                      for editorial in Editorial.query.all()]
        return jsonify({
            'success': True,
            'editorials': editorials,
            'total_series': len(editorials)})

    @app.route('/editorials/<int:id>')
    def get_editorial_detail(id):
        editorial = Editorial.query.filter(Editorial.id == id).one_or_none()
        if editorial is None:
            abort(404)
        return jsonify({
            'success': True,
            'editorial': editorial.format()
        })

    @app.route('/editorials', methods=['POST'])
    def create_editorial():
        data = request.get_json()
        name = data.get('name', None)
        address = data.get('address', None)
        mail = data.get('mail', None)
        editorial = Editorial(name, mail, address)
        try:
            editorial.insert()
            return jsonify({
                'success': True,
                'id_editorial': editorial.id
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    @app.route('/editorials/<int:id>', methods=['DELETE'])
    def delete_editorials(id):
        editorial = Editorial.query.filter(Editorial.id == id).one_or_none()
        if editorial is None:
            abort(404)
        try:
            editorial.delete()
            return jsonify({
                'success': True,
                'id_editorial': id
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    @app.route('/editorials/<int:id>', methods=['PATCH'])
    def update_editorial(id):

        editorial = Editorial.query.filter(Editorial.id == id).one_or_none()
        if editorial is None:
            abort(404)
        data = request.get_json()
        editorial.name = data.get('name', editorial.name)
        editorial.address = data.get('address', editorial.address)
        editorial.mail = data.get('mail', editorial.mail)
        try:
            editorial.update()
            return jsonify({
                'success': True,
                'editorial': editorial.format()
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
