import pytest

import sqlparse
from sqlparse.engine import grouping
from sqlparse.exceptions import SQLParseError


def test_set_max_grouping_tokens_updates_grouping_limit():
    original_limit = grouping.MAX_GROUPING_TOKENS
    try:
        sqlparse.set_max_grouping_tokens(20000)
        assert grouping.MAX_GROUPING_TOKENS == 20000

        sqlparse.set_max_grouping_tokens(None)
        assert grouping.MAX_GROUPING_TOKENS is None
    finally:
        grouping.MAX_GROUPING_TOKENS = original_limit


def test_set_max_grouping_tokens_rejects_nonpositive_limit():
    with pytest.raises(ValueError, match="positive integer or None"):
        sqlparse.set_max_grouping_tokens(0)


def test_set_max_grouping_tokens_controls_parser_guard():
    original_limit = grouping.MAX_GROUPING_TOKENS
    statement = "SELECT " + ", ".join(f"column_{i}" for i in range(20))

    try:
        sqlparse.set_max_grouping_tokens(5)
        with pytest.raises(SQLParseError, match="Maximum number of tokens exceeded"):
            sqlparse.parse(statement)

        sqlparse.set_max_grouping_tokens(100)
        assert len(sqlparse.parse(statement)) == 1
    finally:
        grouping.MAX_GROUPING_TOKENS = original_limit
