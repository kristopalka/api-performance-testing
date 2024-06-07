# coding: utf-8

from fastapi.testclient import TestClient


from src.openapi_server.models.fibonacci import Fibonacci  # noqa: F401
from src.openapi_server.models.message import Message  # noqa: F401


def test_database_get(client: TestClient):
    """Test case for database_get

    Returns random element from database
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/database",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_fibonacci_n_get(client: TestClient):
    """Test case for fibonacci_n_get

    Returns n-th element of Fibonacci Sequence in a JSON object
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/fibonacci/{n}".format(n=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_hello_get(client: TestClient):
    """Test case for hello_get

    Returns simple JSON object with \"Hello World!\" text
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/hello",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

