import os, tempfile
import pytest

from digital_cookbook import digital_cookbook as flaskr


@pytest.fixture
def client():
    db_fd, flaskr.app.config["DATABASE"] = tempfile.mkstemp()
    flaskr.app.config["TESTING"] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config["DATABASE"])


def test_empty_db(client):
    rv = client.get("/")
    assert b"No entries here so far" in rv.data
