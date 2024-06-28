import pytest

from app.users.enums import Role
from tests.assertion_helpers.user import assert_user_out_dict


@pytest.mark.db
def test_register_user(client):
    email = "test@example.com"
    password = "password"

    response = client.post(
        "/api/v1/users/register",
        json={"email": email, "password": password},
    )

    assert response.status_code == 201
    assert_user_out_dict(
        response.json(),
        {
            "email": email,
            "role": Role.USER,
        },
    )
