import os
from flask import Flask, request, jsonify, abort,\
    redirect, url_for, render_template
from models import setup_db, db, Comic, Series, Editorial
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import exc
from auth import requires_auth, AUTH0_DOMAIN,\
    API_AUDIENCE, REDIRECT_URL, CLIENT_ID, AuthError

RESULTS_PER_PAGE = int(os.environ['RESULTS_PER_PAGE'])


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate = Migrate(app, db)

    """CORS initialization"""
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    """ MEthods concerning comics"""
    def paginate_results(results, request):
        page = request.args.get('page', type=int)
        if page is None:
            return results
        else:
            start = (page-1)*RESULTS_PER_PAGE
            end = start+RESULTS_PER_PAGE
            return results[start:end]

    @app.route('/')
    def get_status():
        return "API is running and healthy"

    @app.route('/login')
    def get_login():
        login_url = 'https://{}/authorize?audience={}'\
            '&response_type=token'\
            '&client_id={}&redirect_uri={}/login_detail'.format(
                AUTH0_DOMAIN, API_AUDIENCE, CLIENT_ID, REDIRECT_URL)
        return redirect(login_url)

    @app.route('/login_detail')
    def login_detail():
        return render_template('login_detail.html')

    """ START API's METHODS """

    @app.route('/comics')
    @requires_auth('get:info')
    def get_comics(payload):
        comics = paginate_results([comic.format()
                                   for comic in Comic.query.all()], request)
        if len(comics) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'comics': comics,
            'total_comics': len(comics)
        })

    @app.route('/comics/<int:id>')
    @requires_auth('get:info')
    def get_comic_detail(payload, id):
        comic = Comic.query.filter(Comic.id == id).one_or_none()
        if comic is None:
            abort(404)
        return jsonify({
            'success': True,
            'comic': comic.format()
        })

    @app.route('/comics', methods=['POST'])
    @requires_auth('post:comic')
    def create_comic(payload):
        data = request.get_json()
        name = data.get('name', None)
        synopsis = data.get('synopsis', None)
        characters = data.get('characters', None)
        series_id = data.get('series_id', None)
        serie = Series.query.filter(
            Series.id == series_id).one_or_none()
        """We must check if the series exists
         if not we abort with error PRecondition failed"""
        if serie is None:
            abort(412)

        try:
            comic = Comic(name, synopsis, characters, series_id)
            comic.insert()
            return jsonify({
                'success': True,
                'id_comic': comic.id
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    @app.route('/comics/<int:id>', methods=['DELETE'])
    @requires_auth('delete:comic')
    def delete_comic(payload, id):
        comic = Comic.query.filter(Comic.id == id).one_or_none()
        if comic is None:
            abort(404)
        try:
            comic.delete()
            return jsonify({
                'success': True,
                'id_comic': id
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    @app.route('/comics/<int:id>', methods=['PATCH'])
    @requires_auth('patch:comic')
    def update_comic(payload, id):
        comic = Comic.query.filter(Comic.id == id).one_or_none()
        if comic is None:
            abort(404)
        data = request.get_json()
        comic.name = data.get('name', comic.name)
        comic.sysnopis = data.get('synopsis', comic.synopsis)
        comic.characters = data.get('characters', comic.characters)
        comic.series_id = data.get('series_id', comic.series_id)
        try:
            comic.update()
            return jsonify({
                'success': True,
                'comic': comic.format()
            })
        except exc.SQLAlchemyError as sae:
            print(sae)
            abort(422)

    """Methods concerning the series"""
    @app.route('/series')
    @requires_auth('get:info')
    def get_series(payload):
        series = paginate_results([serie.format()
                                   for serie in Series.query.all()], request)
        if len(series) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'series': series,
            'total_series': len(series)})

    @app.route('/series/<int:id>')
    @requires_auth('get:info')
    def get_series_detail(payload, id):
        serie = Series.query.filter(Series.id == id).one_or_none()
        if serie is None:
            abort(404)
        return jsonify({
            'success': True,
            'serie': serie.format()
        })

    @app.route('/series', methods=['POST'])
    @requires_auth('post:series')
    def create_series(payload):
        data = request.get_json()
        name = data.get('name', None)
        editorial_id = data.get('editorial_id', None)
        editorial = Editorial.query.filter(
            Editorial.id == editorial_id).one_or_none()
        """We must check if the editorial exists
        if not we abort with error PRecondition failed"""
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
    @requires_auth('delete:series')
    def delete_series(payload, id):
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
    @requires_auth('patch:series')
    def update_series(payload, id):
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
    @requires_auth('get:info')
    def get_editorials(payload):
        editorials = paginate_results(
            [editorial.format() for editorial in Editorial.query.all()],
            request
        )
        if len(editorials) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'editorials': editorials,
            'total_editorials': len(editorials)})

    @app.route('/editorials/<int:id>')
    @requires_auth('get:info')
    def get_editorial_detail(payload, id):
        editorial = Editorial.query.filter(Editorial.id == id).one_or_none()
        if editorial is None:
            abort(404)
        return jsonify({
            'success': True,
            'editorial': editorial.format()
        })

    @app.route('/editorials', methods=['POST'])
    @requires_auth('post:editorial')
    def create_editorial(payload):
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
    @requires_auth('delete:editorial')
    def delete_editorials(payload, id):
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
    @requires_auth('patch:editorial')
    def update_editorial(payload,   id):

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

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(412)
    def precondition_fail(error):
        return jsonify({
            "success": False,
            "error": 412,
            "message": "Precondition Failed"
        }), 412

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.args[1],
            'message': error.args[0]
        }), error.args[1]

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
