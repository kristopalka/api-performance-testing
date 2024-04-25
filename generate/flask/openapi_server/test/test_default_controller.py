import unittest

from flask import json

from openapi_server.models.response import Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_hello_get(self):
        """Test case for hello_get

        Returns simple text
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/hello',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
