import os
from flask import Flask
from models import setup_db,db
from flask_cors import CORS
from flask_migrate import Migrate
def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate = Migrate(app, db)
    """ MEthods concerning comics"""
    @app.route('/comics')
    def get_comics():
        return "Devolverá una lista de los comics completa"

    @app.route('/comics/<int:id>')
    def get_comic_detail(id):
        return "El detalle de un comic en concreto"
    
    @app.route('/comics', methods="['POST']")
    def create_comic():
        return "Success=True y el id del comic insertado si todo ha ido bien"

    @app.route('/comics/<int:id>',methods=['DELETE'])
    def delete_comic(id):
        return "Borra un comic"
    
    @app.route('/comics/<int:id>',methods=['PATCH'])
    def update_comic(id):
        return "actualiza el comic"


    """Methods concerning the series"""    
    @app.route('/series')
    def get_series():
        return "Devolverá una lista de los comics completa"

    @app.route('/series/<int:id>')
    def get_series_detail(id):
        return "El detalle de un comic en concreto"
    
    @app.route('/series', methods="['POST']")
    def create_series():
        return "Success=True y el id del comic insertado si todo ha ido bien"

    @app.route('/series/<int:id>',methods=['DELETE'])
    def delete_series(id):
        return "Borra un comic"
    
    @app.route('/series/<int:id>',methods=['PATCH'])
    def update_series(id):
        return "actualiza el comic"

    """ Methods concerning the editorials"""
    @app.route('/editorials')
    def get_editorial():
        return "Devolverá una lista de los comics completa"

    @app.route('/editorials/<int:id>')
    def get_editorial_detail(id):
        return "El detalle de un comic en concreto"
    
    @app.route('/editorials', methods="['POST']")
    def create_editorial():
        return "Success=True y el id del comic insertado si todo ha ido bien"

    @app.route('/editorials/<int:id>',methods=['DELETE'])
    def delete_editorials(id):
        return "Borra un comic"
    
    @app.route('/editorials/<int:id>',methods=['PATCH'])
    def update_editorial(id):
        return "actualiza el comic"

    return app


app = create_app()

if __name__ == '__main__':
    app.run()