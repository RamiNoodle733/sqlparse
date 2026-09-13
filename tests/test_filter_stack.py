from sqlparse import engine, tokens as T
from sqlparse.lexer import Lexer


class CustomLexer(Lexer):
    def get_tokens(self, text, encoding=None):
        yield T.Name, f'custom:{text}'


def test_filter_stack_uses_custom_lexer():
    stack = engine.FilterStack()
    stack.lexer = CustomLexer()

    statements = tuple(stack.run('input'))

    assert len(statements) == 1
    assert str(statements[0]) == 'custom:input'
