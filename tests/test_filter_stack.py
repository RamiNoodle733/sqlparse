from sqlparse import engine, tokens
from sqlparse.lexer import Lexer


def test_filter_stack_allows_custom_lexer():
    custom_lexer = Lexer()
    custom_lexer.default_initialization()
    custom_lexer.add_keywords({'CUSTOMLEXERKEYWORD': tokens.Keyword})

    stack = engine.FilterStack()
    stack.lexer = custom_lexer
    statement = next(stack.run('CUSTOMLEXERKEYWORD value'))

    assert statement.tokens[0].ttype is tokens.Keyword
