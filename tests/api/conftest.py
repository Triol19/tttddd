from typing import AsyncGenerator, cast

import pytest
from databases import Database
from fastapi import FastAPI
from fastapi.testclient import TestClient
from requests import Session

from tttddd.app import create_app


@pytest.fixture
def app(
        engine: AsyncGenerator[Database, None],
) -> FastAPI:
    return cast(FastAPI, create_app())


@pytest.fixture
def client(app: FastAPI) -> Session:
    return TestClient(app)
