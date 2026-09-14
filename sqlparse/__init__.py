#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This module is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

"""Parse SQL statements."""

# Setup namespace
from typing import Any, Generator, IO, List, Optional, Tuple, Union

from sqlparse import sql
from sqlparse import cli
from sqlparse import engine
from sqlparse import tokens
from sqlparse import filters
from sqlparse import formatter
from sqlparse.engine import grouping as _grouping


__version__ = "0.5.6.dev0"
__all__ = [
    "engine",
    "filters",
    "formatter",
    "sql",
    "tokens",
    "cli",
    "set_max_grouping_tokens",
]


def set_max_grouping_tokens(limit: Optional[int]) -> None:
    """Set the maximum token count accepted by the grouping stage.

    Pass ``None`` to disable the token-count limit. Positive integers set a
    process-wide limit for subsequent parsing and formatting operations.
    Disabling or increasing this limit is not recommended for SQL from
    untrusted sources.
    """
    if limit is not None and (
        isinstance(limit, bool) or not isinstance(limit, int) or limit < 1
    ):
        raise ValueError("Grouping token limit must be a positive integer or None")
    _grouping.MAX_GROUPING_TOKENS = limit


def parse(
    sql: str, encoding: Optional[str] = None
) -> Tuple[sql.Statement, ...]:
    """Parse sql and return a list of statements.

    :param sql: A string containing one or more SQL statements.
    :param encoding: The encoding of the statement (optional).
    :returns: A tuple of :class:`~sqlparse.sql.Statement` instances.
    """
    return tuple(parsestream(sql, encoding))


def parsestream(
    stream: Union[str, IO[str]], encoding: Optional[str] = None
) -> Generator[sql.Statement, None, None]:
    """Parses sql statements from file-like object.

    :param stream: A file-like object.
    :param encoding: The encoding of the stream contents (optional).
    :returns: A generator of :class:`~sqlparse.sql.Statement` instances.
    """
    stack = engine.FilterStack()
    stack.enable_grouping()
    return stack.run(stream, encoding)


def format(sql: str, encoding: Optional[str] = None, **options: Any) -> str:
    """Format *sql* according to *options*.

    Available options are documented in :ref:`formatting`.

    In addition to the formatting options this function accepts the
    keyword "encoding" which determines the encoding of the statement.

    :returns: The formatted SQL statement as string.
    """
    stack = engine.FilterStack()
    options = formatter.validate_options(options)
    stack = formatter.build_filter_stack(stack, options)
    stack.postprocess.append(filters.SerializerUnicode())
    return "".join(stack.run(sql, encoding))


def split(
    sql: str, encoding: Optional[str] = None, strip_semicolon: bool = False
) -> List[str]:
    """Split *sql* into single statements.

    :param sql: A string containing one or more SQL statements.
    :param encoding: The encoding of the statement (optional).
    :param strip_semicolon: If True, remove trailing semicolons
        (default: False).
    :returns: A list of strings.
    """
    stack = engine.FilterStack(strip_semicolon=strip_semicolon)
    return [str(stmt).strip() for stmt in stack.run(sql, encoding)]
