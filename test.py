import unittest
import requests
import json
from io import StringIO
import logging
import configparser
config = configparser.ConfigParser()
config.read('superuser.ini')


logging.basicConfig(level=logging.DEBUG, filename='test.log', filemode='w')
logger = logging.getLogger()


class LogCaptureResult(unittest._TextTestResult):

    def _exc_info_to_string(self, err, test):
        tb = super(LogCaptureResult, self)._exc_info_to_string(err, test)
        captured_log = test.stream.getvalue()
        return '\n'.join([tb, 'CAPTURED LOG', '=' * 70, captured_log])


class LogCaptureRunner(unittest.TextTestRunner):

    def _makeResult(self):
        return LogCaptureResult(self.stream, self.descriptions, self.verbosity)


class TestBaseAuth(unittest.TestCase):
    @classmethod
    def get_token(cls):
        response = requests.post(
            'http://localhost:8080/token-auth',
            data=json.dumps({
                    "username": config['DEFAULT']['username'],
                    "password": config['DEFAULT']['password']
                    })
        )
        response = json.loads(response.content)
        token = response['token']
        return token

    def test_get_token(self):
        try:
            token = self.get_token()
            res = True
        except Exception as e:
            res = False
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        logger.addHandler(self.handler)
        self.assertEqual(True, res)

    def test_token_verify(self):
        try:
            token = self.get_token()
            response = requests.get('http://localhost:8080/token-verify',
                                    headers={"authorization": token})
            response = json.loads(response.content)
            if response == {'message': 'Token is valid'}:
                res = True
            else:
                res = False
        except Exception as e:
            res = False
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        logger.addHandler(self.handler)
        self.assertEqual(True, res)

    def test_token_refresh(self):
        try:
            token = self.get_token()
            response = requests.post('http://localhost:8080/token-refresh',
                                     headers={"authorization": token})
            response = json.loads(response.content)
            token = response['token']
            res = True
        except Exception as e:
            res = False
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        logger.addHandler(self.handler)
        self.assertEqual(True, res)

    def test_get_current_user(self):
        try:
            token = self.get_token()
            response = requests.get('http://localhost:8080/current-user',
                                    headers={"authorization": token})
            response = json.loads(response.content)
            if response['username'] == config['DEFAULT']['username']:
                res = True
            else:
                res = False
        except Exception as e:
            res = False
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        logger.addHandler(self.handler)
        self.assertEqual(True, res)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBaseAuth)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)
