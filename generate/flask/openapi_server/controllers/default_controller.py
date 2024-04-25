import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.response import Response  # noqa: E501
from openapi_server import util


def hello_get():  # noqa: E501
    """Returns simple text

     # noqa: E501


    :rtype: Union[Response, Tuple[Response, int], Tuple[Response, int, Dict[str, str]]
    """
    return Response("Hello world!")
