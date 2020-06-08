import base64

import ast

import unittest

from app import app


class TestCase(unittest.TestCase):
    def test_server_live(self):
        tester = app.test_client(self)
        r = tester.get('/')

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data.decode(), 'GET Success!\n')

    def test_responses(self):
        # define variables
        tester = app.test_client(self)
        name = 'Jane Doe'
        headers = {'Content-Type': 'application/json', 'ce-id': 'test-id'}

        # base64 encode data
        string_encoding = base64.b64encode(name.encode()).decode()
        body = {'message': {'data': string_encoding}}

        # make request
        r = tester.post('/', json=body, headers=headers)

        # read request
        data = ast.literal_eval(r.data.decode())
        response_message = data['message']

        self.assertEqual(r.status_code, 200)
        self.assertEqual(response_message, 'Hello {0}! ID: {1}'.format(
            name,
            headers['ce-id']
        ))

    def test_missing_id_header(self):
        # define variables
        tester = app.test_client(self)
        name = 'Jane Doe'
        headers = {'Content-Type': 'application/json'}

        # base64 encode data
        string_encoding = base64.b64encode(name.encode()).decode()
        body = {'message': {'data': string_encoding}}

        # make request
        r = tester.post('/', json=body, headers=headers)

        # read request
        data = ast.literal_eval(r.data.decode())

        self.assertEqual(r.status_code, 400)
        self.assertEqual(data['err'], 'missing ce-id field in Pub/Sub headers')

    def test_missing_message_field(self):
        # define variables
        tester = app.test_client(self)
        name = 'Jane Doe'
        headers = {'Content-Type': 'application/json'}

        # base64 encode data
        string_encoding = base64.b64encode(name.encode()).decode()
        body = {'not-message': {'data': string_encoding}}

        # make request
        r = tester.post('/', json=body, headers=headers)

        # read request
        data = ast.literal_eval(r.data.decode())

        self.assertEqual(r.status_code, 400)
        self.assertEqual(data['err'], 'invalid Pub/Sub message format')

    def test_missing_data_field(self):
        # define variables
        tester = app.test_client(self)
        name = 'Jane Doe'
        headers = {'Content-Type': 'application/json', 'ce-id': 'test-id'}

        # base64 encode data
        string_encoding = base64.b64encode(name.encode()).decode()
        body = {'message': {'not-data': string_encoding}}

        # make request
        r = tester.post('/', json=body, headers=headers)

        # read request
        data = ast.literal_eval(r.data.decode())

        self.assertEqual(r.status_code, 400)
        self.assertEqual(data['err'], 'invalid Pub/Sub message format')


if __name__ == '__main__':
    unittest.main()
