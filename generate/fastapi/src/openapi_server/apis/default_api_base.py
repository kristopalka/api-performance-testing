# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.fibonacci import Fibonacci
from openapi_server.models.message import Message


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    def database_get(
        self,
    ) -> Message:
        ...


    def fibonacci_n_get(
        self,
        n: int,
    ) -> Fibonacci:
        ...


    def hello_get(
        self,
    ) -> Message:
        ...
