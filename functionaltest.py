#things that we need to use
import unittest
import json

#load our application
from app import app as tested_app

class TestApp(unittest.TestCase):
    def test_help(self):
        # creating a FlaskClient instance to interact with the app
        app = tested_app.test_client()

        # calling /api/ endpoint
        hello = app.get('/api/hello/')

        # asserting the body
        body = json.loads(str(hello.data, 'utf8'))

        # the value of the Hello key should be default
        self.assertEqual(body['Hello'], 'World!')

    def test_version(self):
        app = tested_app.test_client()
        version = app.get('/api/version/')
        self.assertEqual(version.status_code, 200)
        body = json.loads(str(version.data, 'utf8'))
        self.assertEqual(body['version'], 'na')

    def test_home(self):
        app = tested_app.test_client()
        self.assertEqual(app.get('/').status_code, 200)

if __name__ == '__main__':
    unittest.main()
