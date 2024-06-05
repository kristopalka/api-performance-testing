# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.fibonacci import Fibonacci
from openapi_server.models.message import Message


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/database",
    responses={
        200: {"model": Message, "description": "successful operation"},
    },
    tags=["default"],
    summary="Returns random element from database",
    response_model_by_alias=True,
)
async def database_get(
) -> Message:
    ...


@router.get(
    "/fibonacci/{n}",
    responses={
        200: {"model": Fibonacci, "description": "successful operation"},
    },
    tags=["default"],
    summary="Returns n-th element of Fibonacci Sequence in a JSON object",
    response_model_by_alias=True,
)
async def fibonacci_n_get(
    n: int = Path(..., description="number of Fibonacci element to return"),
) -> Fibonacci:
    ...


@router.get(
    "/hello",
    responses={
        200: {"model": Message, "description": "successful operation"},
    },
    tags=["default"],
    summary="Returns simple JSON object with \&quot;Hello World!\&quot; text",
    response_model_by_alias=True,
)
async def hello_get(
) -> Message:
    ...
