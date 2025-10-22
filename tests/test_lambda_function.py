"""Test Lambda function handler module (non-Alexa)."""

import pytest

from lambda_function import lambda_handler
from lambda_function.alexa import _text_output


def test_no_query():
    """Test that if no query is provided, the lambda_handler correctly returns
    a fail message."""
    response = lambda_handler({}, None)
    assert response["status"] == "fail" and "fail" in response["data"]
    assert (
        _text_output(group="api", key="no_query") in response["data"]["fail"]
    )


@pytest.mark.parametrize("body", [None, [], "str"])
def test_invalid_body(body):
    """Test that if an invalid body is provided, the lambda_handler correctly
    returns a fail message."""
    response = lambda_handler({"body": body}, None)
    assert response["status"] == "fail" and "fail" in response["data"]
    assert (
        _text_output(group="api", key="invalid_body")
        in response["data"]["fail"]
    )


@pytest.mark.parametrize(
    "query, expected",
    [
        ("What are some antonyms of 'happy'?", "sad"),
        ("I need to check the mail", "done"),
        ("Add potato to the shopping list", "done"),
    ],
)
def test_query(query, expected):
    """Test that if a valid query is provided, the API response successfully
    returns a response."""
    response = lambda_handler({"body": {"query": query}}, None)
    assert "status" in response
    assert response["status"] == "success"
    assert expected in response["data"]["text"].lower()
