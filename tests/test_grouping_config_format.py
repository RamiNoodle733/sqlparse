import pytest

import sqlparse
from sqlparse.engine import grouping
from sqlparse.exceptions import SQLParseError


def test_set_max_grouping_tokens_applies_to_formatting():
    original = grouping.MAX_GROUPING_TOKENS
    try:
        sqlparse.set_max_grouping_tokens(1)
        with pytest.raises(SQLParseError, match="Maximum number of tokens exceeded"):
            sqlparse.format("select value from example", reindent=True)
    finally:
        grouping.MAX_GROUPING_TOKENS = original
