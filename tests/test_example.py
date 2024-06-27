from app.config import env_file


def test_example():
    assert env_file == ".env.test"
