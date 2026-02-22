"""
Test Lexer Module
Tests for Pyrl lexer functionality.
"""
import pytest
from src.core.lexer import tokenize, Lexer
from src.core.ast_nodes import TokenType
from src.core.exceptions import LexerError


class TestLexerBasics:
    """Basic lexer tests."""
    
    def test_empty_source(self):
        """Test tokenizing empty source."""
        tokens = tokenize("")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_whitespace_only(self):
        """Test tokenizing whitespace only."""
        tokens = tokenize("   \t   ")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_single_number(self):
        """Test tokenizing a single number."""
        tokens = tokenize("42")
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 42.0
    
    def test_float_number(self):
        """Test tokenizing a float."""
        tokens = tokenize("3.14")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 3.14
    
    def test_single_string(self):
        """Test tokenizing a single string."""
        tokens = tokenize('"hello"')
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"
    
    def test_single_string_single_quote(self):
        """Test tokenizing a single-quoted string."""
        tokens = tokenize("'world'")
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "world"


class TestLexerSigils:
    """Tests for sigil variables."""
    
    def test_scalar_variable(self):
        """Test tokenizing scalar variable."""
        tokens = tokenize("$name")
        assert tokens[0].type == TokenType.SCALAR
        assert tokens[0].value == "name"
    
    def test_array_variable(self):
        """Test tokenizing array variable."""
        tokens = tokenize("@items")
        assert tokens[0].type == TokenType.ARRAY
        assert tokens[0].value == "items"
    
    def test_hash_variable(self):
        """Test tokenizing hash variable."""
        tokens = tokenize("%person")
        assert tokens[0].type == TokenType.HASH
        assert tokens[0].value == "person"
    
    def test_function_reference(self):
        """Test tokenizing function reference."""
        tokens = tokenize("&myfunc")
        assert tokens[0].type == TokenType.FUNCTION
        assert tokens[0].value == "myfunc"


class TestLexerKeywords:
    """Tests for keywords."""
    
    def test_if_keyword(self):
        """Test if keyword."""
        tokens = tokenize("if")
        assert tokens[0].type == TokenType.IF
    
    def test_else_keyword(self):
        """Test else keyword."""
        tokens = tokenize("else")
        assert tokens[0].type == TokenType.ELSE
    
    def test_while_keyword(self):
        """Test while keyword."""
        tokens = tokenize("while")
        assert tokens[0].type == TokenType.WHILE
    
    def test_for_keyword(self):
        """Test for keyword."""
        tokens = tokenize("for")
        assert tokens[0].type == TokenType.FOR
    
    def test_def_keyword(self):
        """Test def keyword."""
        tokens = tokenize("def")
        assert tokens[0].type == TokenType.DEF
    
    def test_return_keyword(self):
        """Test return keyword."""
        tokens = tokenize("return")
        assert tokens[0].type == TokenType.RETURN
    
    def test_print_keyword(self):
        """Test print keyword."""
        tokens = tokenize("print")
        assert tokens[0].type == TokenType.PRINT
    
    def test_true_false_none(self):
        """Test boolean and none literals."""
        tokens = tokenize("True False None")
        assert tokens[0].type == TokenType.TRUE
        assert tokens[1].type == TokenType.FALSE
        assert tokens[2].type == TokenType.NONE


class TestLexerOperators:
    """Tests for operators."""
    
    def test_arithmetic_operators(self):
        """Test arithmetic operators."""
        tokens = tokenize("+ - * / %")
        assert tokens[0].type == TokenType.PLUS
        assert tokens[1].type == TokenType.MINUS
        assert tokens[2].type == TokenType.STAR
        assert tokens[3].type == TokenType.SLASH
        assert tokens[4].type == TokenType.PERCENT
    
    def test_power_operator(self):
        """Test power operator."""
        tokens = tokenize("**")
        assert tokens[0].type == TokenType.STARSTAR
    
    def test_floor_division(self):
        """Test floor division operator."""
        tokens = tokenize("//")
        assert tokens[0].type == TokenType.DOUBLESLASH
    
    def test_comparison_operators(self):
        """Test comparison operators."""
        tokens = tokenize("== != < <= > >=")
        assert tokens[0].type == TokenType.EQ
        assert tokens[1].type == TokenType.NE
        assert tokens[2].type == TokenType.LT
        assert tokens[3].type == TokenType.LE
        assert tokens[4].type == TokenType.GT
        assert tokens[5].type == TokenType.GE
    
    def test_assignment_operators(self):
        """Test assignment operators."""
        tokens = tokenize("= += -= *= /=")
        assert tokens[0].type == TokenType.ASSIGN
        assert tokens[1].type == TokenType.PLUS_ASSIGN
        assert tokens[2].type == TokenType.MINUS_ASSIGN
        assert tokens[3].type == TokenType.STAR_ASSIGN
        assert tokens[4].type == TokenType.SLASH_ASSIGN


class TestLexerDelimiters:
    """Tests for delimiters."""
    
    def test_parentheses(self):
        """Test parentheses."""
        tokens = tokenize("()")
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.RPAREN
    
    def test_brackets(self):
        """Test brackets."""
        tokens = tokenize("[]")
        assert tokens[0].type == TokenType.LBRACKET
        assert tokens[1].type == TokenType.RBRACKET
    
    def test_braces(self):
        """Test braces."""
        tokens = tokenize("{}")
        assert tokens[0].type == TokenType.LBRACE
        assert tokens[1].type == TokenType.RBRACE
    
    def test_comma_colon_dot(self):
        """Test comma, colon, and dot."""
        tokens = tokenize(", : .")
        assert tokens[0].type == TokenType.COMMA
        assert tokens[1].type == TokenType.COLON
        assert tokens[2].type == TokenType.DOT
    
    def test_arrow(self):
        """Test arrow operator."""
        tokens = tokenize("->")
        assert tokens[0].type == TokenType.ARROW


class TestLexerIndentation:
    """Tests for indentation handling."""
    
    def test_indent_dedent(self):
        """Test indent and dedent tokens."""
        source = """if True:
    $x = 1
"""
        tokens = tokenize(source)
        token_types = [t.type for t in tokens]
        assert TokenType.INDENT in token_types
        assert TokenType.DEDENT in token_types
    
    def test_nested_indentation(self):
        """Test nested indentation."""
        source = """if True:
    if True:
        $x = 1
"""
        tokens = tokenize(source)
        token_types = [t.type for t in tokens]
        assert token_types.count(TokenType.INDENT) == 2
        assert token_types.count(TokenType.DEDENT) == 2


class TestLexerComments:
    """Tests for comments."""
    
    def test_line_comment(self):
        """Test line comment."""
        tokens = tokenize("$x = 1  # This is a comment")
        # Comment should be ignored
        assert all(t.type != TokenType.IDENTIFIER or t.value != "comment" for t in tokens)
    
    def test_comment_only_line(self):
        """Test comment-only line."""
        tokens = tokenize("# Only a comment\n$x = 1")
        assert tokens[0].type == TokenType.SCALAR


class TestLexerErrors:
    """Tests for lexer errors."""
    
    def test_invalid_character(self):
        """Test invalid character raises error."""
        with pytest.raises(LexerError):
            tokenize("@")  # @ without identifier
    
    def test_unterminated_string(self):
        """Test unterminated string raises error."""
        with pytest.raises(LexerError):
            tokenize('"unterminated')


@pytest.mark.lexer
class TestLexerComplex:
    """Complex lexer tests."""
    
    def test_expression(self):
        """Test tokenizing a complex expression."""
        tokens = tokenize("$x = 1 + 2 * 3")
        assert len(tokens) > 5
        
    def test_function_call(self):
        """Test tokenizing function call."""
        tokens = tokenize("print($name)")
        assert tokens[0].type == TokenType.PRINT
        
    def test_array_literal(self):
        """Test tokenizing array literal."""
        tokens = tokenize("[1, 2, 3]")
        assert tokens[0].type == TokenType.LBRACKET
        
    def test_hash_literal(self):
        """Test tokenizing hash literal."""
        tokens = tokenize('{"key": "value"}')
        assert tokens[0].type == TokenType.LBRACE
