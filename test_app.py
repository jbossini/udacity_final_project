import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Comic, Series, Editorial


class ComiqueaTestCase(unittest.TestCase):
    """ This class represent the Comic API test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get("DATABASE_URL")+"_test"
        setup_db(self.app, self.database_path)
        self.EDITOR_AUTHORIZATION_TOKEN = os.environ.get(
            "EDITOR_AUTHORIZATION_TOKEN")
        self.FAN_AUTHORIZATION_TOKEN = os.environ.get(
            "FAN_AUTHORIZATION_TOKEN")
        self.WRITER_AUTHORIZATION_TOKEN = os.environ.get(
            "WRITER_AUTHORIZATION_TOKEN")

        self.new_comic={
            "name":"Zipi y Zape",
            "synopsys":"Two twins are always getting in trouble",
            "characters":"Zipy y Zape",
            "series_id":1
            }
        self.bad_comic={
            "name":"Zipi y Zape",
            "synopsys":"Two twins are always getting in trouble",
            "characters":"Zipy y Zape",
            "series_id":1000
            }
        self.new_series={
            "name":"Super Húmor",
            "editorial_id":1
        }
        self.bad_series={
            "name":"Super Húmor",
            "editorial_id":1000
        }
        self.new_editorial={
            "name":"Planeta de Agostini",
            "address":"Spain",
            "mail":"pda@planeta.es"
        }
        self.bad_editorial={
            "name":"Planeta de Agostini",
            "address":"Spain"
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    
     
    def test_get_comics_OK(self):
        res = self.client().get(
            '/comics', headers={
                "Authorization": f"Bearer {self.FAN_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['comics'])
    
    def test_get_comics_error_404(self):
        res = self.client().get(
            '/comics?page=1000', headers={
                "Authorization": f"Bearer {self.FAN_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

    def test_get_comics_detail_OK(self):
        res = self.client().get(
            '/comics/1', headers={
                "Authorization": f"Bearer {self.FAN_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['comic'])
    
    def test_get_comic_detail_error_404(self):
        res = self.client().get(
            '/comics/1000', headers={
                "Authorization": f"Bearer {self.FAN_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    
    def test_post_comic(self):
        res = self.client().post(
            '/comics',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            },
            json=self.new_comic)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_comic'])

    def test_post_comic_series_not_found(self):
        res = self.client().post(
            '/comics',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            },
            json=self.bad_comic)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    
    def test_patch_comic(self):
        res = self.client().patch(
            '/comics/2',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            },json={"name":"Mortadelo y Filemón"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['comic'])

    def test_patch_comic_not_found(self):
        res = self.client().patch(
            '/comics/1000',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            },json={"name":"Mortadelo y Filemon"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error']) 
    def test_delete_comic(self):
        res = self.client().delete(
            '/comics/3',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_comic'])

    def test_delete_comic_not_found(self):
        res = self.client().delete(
            '/comics/1000',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    

    """Test concerning the series """
    
    def test_get_series_OK(self):
        res = self.client().get(
            '/series', headers={
                "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['series'])
    
    def test_get_series_error_404(self):
        res = self.client().get(
            '/series?page=1000', headers={
                "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

    def test_get_series_detail_OK(self):
        res = self.client().get(
            '/series/1', headers={
                "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['serie'])
    
    def test_get_series_detail_error_404(self):
        res = self.client().get(
            '/series/1000', headers={
                "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    
    def test_post_series(self):
        res = self.client().post(
            '/series',
            headers={
               "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"  
            },
            json=self.new_series)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_serie'])

    def test_post_series_editorial_not_found(self):
        res = self.client().post(
            '/series',
            headers={
               "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"  
            },
            json=self.bad_series)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 412)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    
    def test_patch_serie(self):
        res = self.client().patch(
            '/series/2',
            headers={
               "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"  
            },
            json={"name":"Super Humor"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['serie'])

    def test_patch_serie_not_found(self):
        res = self.client().patch(
            '/series/1000',
            headers={
               "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"  
            },json={"name":"Mortadelo y Filemon"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error']) 
    
    def test_delete_series(self):
        res = self.client().delete(
            '/series/3',
            headers={
               "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"  
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_serie'])

    def test_delete_serie_not_found(self):
        res = self.client().delete(
            '/series/1000',
            headers={
               "Authorization": f"Bearer {self.WRITER_AUTHORIZATION_TOKEN}"  
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    


    def test_get_editorial_OK(self):
        res = self.client().get(
            '/editorials', headers={
                "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['editorials'])
    
    def test_get_editorial_error_404(self):
        res = self.client().get(
            '/editorials?page=1000', headers={
                "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

    def test_get_editorial_detail_OK(self):
        res = self.client().get(
            '/editorials/1', headers={
                "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['editorial'])
    
    def test_get_editorial_detail_error_404(self):
        res = self.client().get(
            '/editorials/1000', headers={
                "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    
    def test_post_editorial(self):
        res = self.client().post(
            '/editorials',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            },
            json=self.new_editorial)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_editorial'])

    def test_post_editorial_sql_error_422(self):
        res = self.client().post(
            '/editorials',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            },
            json=self.bad_editorial)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    
    def test_patch_editorial(self):
        res = self.client().patch(
            '/editorials/2',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            },json={"name":"Planeta"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['editorial'])

    def test_patch_editorial_not_found(self):
        res = self.client().patch(
            '/editorials/1000',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            },json={"name":"Planeta de Agostini"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    def test_delete_editorial(self):
        res = self.client().delete(
            '/editorials/3',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id_editorial'])

    def test_delete_editorial_not_found(self):
        res = self.client().delete(
            '/editorials/1000',
            headers={
               "Authorization": f"Bearer {self.EDITOR_AUTHORIZATION_TOKEN}"  
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
