import pytest

import sqlparse
from sqlparse.engine import grouping
from sqlparse.exceptions import SQLParseError


@pytest.fixture(autouse=True)
def restore_grouping_token_limit():
    original = grouping.MAX_GROUPING_TOKENS
    try:
        yield
    finally:
        grouping.MAX_GROUPING_TOKENS = original


def test_set_max_grouping_tokens_changes_parser_limit():
    sqlparse.set_max_grouping_tokens(1)

    with pytest.raises(SQLParseError, match="Maximum number of tokens exceeded"):
        sqlparse.parse("select value from example")


def test_set_max_grouping_tokens_none_disables_limit():
    sqlparse.set_max_grouping_tokens(None)

    assert len(sqlparse.parse("select value from example")) == 1


@pytest.mark.parametrize("limit", (0, -1, True, 1.5, "100"))
def test_set_max_grouping_tokens_rejects_invalid_values(limit):
    with pytest.raises(
        ValueError,
        match="Grouping token limit must be a positive integer or None",
    ):
        sqlparse.set_max_grouping_tokens(limit)
