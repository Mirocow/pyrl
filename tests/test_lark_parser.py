"""
Test Lark Parser Module
Comprehensive tests for Pyrl Lark-based parser.
"""
import pytest
from src.core.lark_parser import (
    PyrlLarkParser,
    PyrlTransformer,
    PyrlIndenter,
    Program,
    ScalarVar,
    ArrayVar,
    HashVar,
    FuncVar,
    IdentRef,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NoneLiteral,
    ArrayLiteral,
    HashLiteral,
    RegexLiteral,
    BinaryOp,
    UnaryOp,
    Assignment,
    HashAccess,
    ArrayAccess,
    FunctionCall,
    FunctionDef,
    IfStatement,
    ForLoop,
    WhileLoop,
    ReturnStatement,
    PrintStatement,
    AssertStatement,
    TestBlock,
    VueComponent,
    # OOP and Anonymous Functions
    Block,
    AnonymousFuncDef,
    ClassDef,
    MethodDef,
    PropertyDef,
    MethodCall,
    parse_lark,
    parse_file_lark,
    get_parser,
    print_ast,
)


class TestParserBasics:
    """Basic parser tests."""

    def test_create_parser(self):
        """Test creating a parser instance."""
        parser = PyrlLarkParser()
        assert parser is not None
        assert not parser.debug

    def test_create_parser_debug(self):
        """Test creating parser with debug mode."""
        parser = PyrlLarkParser(debug=True)
        assert parser.debug

    def test_parse_empty(self):
        """Test parsing empty source."""
        parser = PyrlLarkParser()
        ast = parser.parse("")
        assert isinstance(ast, Program)
        assert ast.statements == []


class TestNumberParsing:
    """Tests for number literal parsing."""

    def test_integer(self):
        """Test integer parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("42")
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], NumberLiteral)
        assert ast.statements[0].value == 42

    def test_negative_integer(self):
        """Test negative integer parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("-42")
        assert len(ast.statements) == 1
        # Negative is a unary op
        assert isinstance(ast.statements[0], UnaryOp)
        assert ast.statements[0].operator == '-'

    def test_float(self):
        """Test float parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("3.14")
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], NumberLiteral)
        assert ast.statements[0].value == 3.14

    def test_zero(self):
        """Test zero parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("0")
        assert ast.statements[0].value == 0


class TestStringParsing:
    """Tests for string literal parsing."""

    def test_double_quoted_string(self):
        """Test double quoted string parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse('"hello"')
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], StringLiteral)
        assert ast.statements[0].value == "hello"

    def test_single_quoted_string(self):
        """Test single quoted string parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("'world'")
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], StringLiteral)
        assert ast.statements[0].value == "world"

    def test_empty_string(self):
        """Test empty string parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse('""')
        assert ast.statements[0].value == ""

    def test_string_with_escape(self):
        """Test string with escape sequences."""
        parser = PyrlLarkParser()
        ast = parser.parse('"hello\\nworld"')
        assert ast.statements[0].value == "hello\nworld"


class TestBooleanParsing:
    """Tests for boolean literal parsing."""

    def test_true(self):
        """Test True parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("True")
        # True is parsed as IdentRef and resolved to Boolean at runtime
        assert isinstance(ast.statements[0], (BooleanLiteral, IdentRef))

    def test_false(self):
        """Test False parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("False")
        assert isinstance(ast.statements[0], (BooleanLiteral, IdentRef))

    def test_lowercase_true(self):
        """Test lowercase true parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("true")
        assert isinstance(ast.statements[0], (BooleanLiteral, IdentRef))

    def test_lowercase_false(self):
        """Test lowercase false parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("false")
        assert isinstance(ast.statements[0], (BooleanLiteral, IdentRef))


class TestNoneParsing:
    """Tests for None literal parsing."""

    def test_none(self):
        """Test None parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("None")
        # None is parsed as IdentRef and resolved at runtime
        assert isinstance(ast.statements[0], (NoneLiteral, IdentRef))

    def test_null(self):
        """Test null parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("null")
        assert isinstance(ast.statements[0], (NoneLiteral, IdentRef))


class TestVariableParsing:
    """Tests for variable parsing."""

    def test_scalar_var(self):
        """Test scalar variable parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("$x")
        assert isinstance(ast.statements[0], ScalarVar)
        assert ast.statements[0].name == "x"

    def test_array_var(self):
        """Test array variable parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("@arr")
        assert isinstance(ast.statements[0], ArrayVar)
        assert ast.statements[0].name == "arr"

    def test_hash_var(self):
        """Test hash variable parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("%hash")
        assert isinstance(ast.statements[0], HashVar)
        assert ast.statements[0].name == "hash"

    def test_func_var(self):
        """Test function variable parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("&func")
        assert isinstance(ast.statements[0], FuncVar)
        assert ast.statements[0].name == "func"

    def test_identifier_ref(self):
        """Test identifier reference parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("my_func")
        assert isinstance(ast.statements[0], IdentRef)
        assert ast.statements[0].name == "my_func"


class TestArrayParsing:
    """Tests for array literal parsing."""

    def test_empty_array(self):
        """Test empty array parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("[]")
        assert isinstance(ast.statements[0], ArrayLiteral)
        assert ast.statements[0].elements == []

    def test_simple_array(self):
        """Test simple array parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("[1, 2, 3]")
        assert isinstance(ast.statements[0], ArrayLiteral)
        assert len(ast.statements[0].elements) == 3

    def test_mixed_array(self):
        """Test mixed type array parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse('[1, "two", True]')
        assert isinstance(ast.statements[0], ArrayLiteral)
        assert len(ast.statements[0].elements) == 3


class TestHashParsing:
    """Tests for hash literal parsing."""

    def test_empty_hash(self):
        """Test empty hash parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("{}")
        assert isinstance(ast.statements[0], HashLiteral)
        assert ast.statements[0].pairs == {}

    def test_simple_hash(self):
        """Test simple hash parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse('{name: "Alice"}')
        assert isinstance(ast.statements[0], HashLiteral)
        assert "name" in ast.statements[0].pairs

    def test_multi_key_hash(self):
        """Test multi-key hash parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse('{name: "Bob", age: 30}')
        assert isinstance(ast.statements[0], HashLiteral)
        assert "name" in ast.statements[0].pairs
        assert "age" in ast.statements[0].pairs


class TestBinaryOperations:
    """Tests for binary operation parsing."""

    def test_addition(self):
        """Test addition parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("1 + 2")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '+'

    def test_subtraction(self):
        """Test subtraction parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("5 - 3")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '-'

    def test_multiplication(self):
        """Test multiplication parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("4 * 3")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '*'

    def test_division(self):
        """Test division parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("10 / 2")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '/'

    def test_floor_division(self):
        """Test floor division parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("7 // 2")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '//'

    def test_modulo(self):
        """Test modulo parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("7 % 3")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '%'

    def test_comparison(self):
        """Test comparison parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("5 == 5")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '=='

    def test_less_than(self):
        """Test less than parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("3 < 5")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '<'

    def test_greater_than(self):
        """Test greater than parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("5 > 3")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == '>'

    def test_and_operator(self):
        """Test and operator parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("True and False")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == 'and'

    def test_or_operator(self):
        """Test or operator parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("True or False")
        assert isinstance(ast.statements[0], BinaryOp)
        assert ast.statements[0].operator == 'or'


class TestUnaryOperations:
    """Tests for unary operation parsing."""

    def test_negation(self):
        """Test numeric negation parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("-5")
        assert isinstance(ast.statements[0], UnaryOp)
        assert ast.statements[0].operator == '-'

    def test_not(self):
        """Test logical not parsing."""
        parser = PyrlLarkParser()
        ast = parser.parse("!True")
        assert isinstance(ast.statements[0], UnaryOp)
        assert ast.statements[0].operator == '!'


class TestAssignment:
    """Tests for assignment parsing."""

    def test_scalar_assignment(self):
        """Test scalar variable assignment."""
        parser = PyrlLarkParser()
        ast = parser.parse("$x = 10")
        assert isinstance(ast.statements[0], Assignment)
        assert isinstance(ast.statements[0].target, ScalarVar)
        assert ast.statements[0].target.name == "x"

    def test_array_assignment(self):
        """Test array variable assignment."""
        parser = PyrlLarkParser()
        ast = parser.parse("@arr = [1, 2, 3]")
        assert isinstance(ast.statements[0], Assignment)
        assert isinstance(ast.statements[0].target, ArrayVar)

    def test_hash_assignment(self):
        """Test hash variable assignment."""
        parser = PyrlLarkParser()
        ast = parser.parse('%h = {a: 1}')
        assert isinstance(ast.statements[0], Assignment)
        assert isinstance(ast.statements[0].target, HashVar)


class TestIndexAccess:
    """Tests for index access parsing."""

    def test_array_index(self):
        """Test array index access."""
        parser = PyrlLarkParser()
        ast = parser.parse("@arr[0]")
        assert isinstance(ast.statements[0], ArrayAccess)
        assert isinstance(ast.statements[0].obj, ArrayVar)

    def test_hash_key_access(self):
        """Test hash key access."""
        parser = PyrlLarkParser()
        ast = parser.parse('%person["name"]')
        assert isinstance(ast.statements[0], ArrayAccess)


class TestFunctionDefinition:
    """Tests for function definition parsing."""

    def test_no_params(self):
        """Test function with no parameters."""
        parser = PyrlLarkParser()
        ast = parser.parse("""def greet():
    return "Hello"
""")
        assert isinstance(ast.statements[0], FunctionDef)
        assert ast.statements[0].name == "greet"
        assert ast.statements[0].params == []

    def test_with_params(self):
        """Test function with parameters."""
        parser = PyrlLarkParser()
        ast = parser.parse("""def add($a, $b):
    return $a + $b
""")
        assert isinstance(ast.statements[0], FunctionDef)
        assert ast.statements[0].name == "add"
        assert ast.statements[0].params == ["a", "b"]

    def test_sigil_function(self):
        """Test function with & sigil."""
        parser = PyrlLarkParser()
        ast = parser.parse("""&greet():
    return "Hello"
""")
        # & sigil creates an anonymous function definition
        assert isinstance(ast.statements[0], (FunctionDef, AnonymousFuncDef))
        assert ast.statements[0].name == "greet"


class TestFunctionCall:
    """Tests for function call parsing."""

    def test_no_args(self):
        """Test function call with no arguments."""
        parser = PyrlLarkParser()
        ast = parser.parse("greet()")
        assert isinstance(ast.statements[0], FunctionCall)
        assert ast.statements[0].name == "greet"
        assert ast.statements[0].args == []

    def test_with_args(self):
        """Test function call with arguments."""
        parser = PyrlLarkParser()
        ast = parser.parse("add(1, 2)")
        assert isinstance(ast.statements[0], FunctionCall)
        assert ast.statements[0].name == "add"
        assert len(ast.statements[0].args) == 2


class TestIfStatement:
    """Tests for if statement parsing."""

    def test_simple_if(self):
        """Test simple if statement."""
        parser = PyrlLarkParser()
        ast = parser.parse("""if True:
    $x = 1
""")
        assert isinstance(ast.statements[0], IfStatement)
        assert ast.statements[0].condition is not None
        assert len(ast.statements[0].then_body) > 0

    def test_if_else(self):
        """Test if-else statement."""
        parser = PyrlLarkParser()
        ast = parser.parse("""if True:
    $x = 1
else:
    $x = 2
""")
        assert isinstance(ast.statements[0], IfStatement)
        assert ast.statements[0].else_body is not None

    def test_if_elif_else(self):
        """Test if-elif-else statement."""
        parser = PyrlLarkParser()
        ast = parser.parse("""if $x == 1:
    $y = 1
elif $x == 2:
    $y = 2
else:
    $y = 3
""")
        assert isinstance(ast.statements[0], IfStatement)
        assert len(ast.statements[0].elif_clauses) > 0
        assert ast.statements[0].else_body is not None


class TestForLoop:
    """Tests for for loop parsing."""

    def test_simple_for(self):
        """Test simple for loop."""
        parser = PyrlLarkParser()
        ast = parser.parse("""for $i in @arr:
    print($i)
""")
        assert isinstance(ast.statements[0], ForLoop)
        assert ast.statements[0].var == "i"
        assert len(ast.statements[0].body) > 0

    def test_for_with_range(self):
        """Test for loop with range."""
        parser = PyrlLarkParser()
        ast = parser.parse("""for $i in range(5):
    print($i)
""")
        assert isinstance(ast.statements[0], ForLoop)
        assert ast.statements[0].var == "i"


class TestWhileLoop:
    """Tests for while loop parsing."""

    def test_simple_while(self):
        """Test simple while loop."""
        parser = PyrlLarkParser()
        ast = parser.parse("""while $x < 10:
    $x = $x + 1
""")
        assert isinstance(ast.statements[0], WhileLoop)
        assert ast.statements[0].condition is not None
        assert len(ast.statements[0].body) > 0


class TestReturnStatement:
    """Tests for return statement parsing."""

    def test_return_value(self):
        """Test return with value."""
        parser = PyrlLarkParser()
        ast = parser.parse("""def f():
    return 42
""")
        func_def = ast.statements[0]
        assert isinstance(func_def, FunctionDef)
        assert isinstance(func_def.body[0], ReturnStatement)

    def test_return_no_value(self):
        """Test return without value."""
        parser = PyrlLarkParser()
        ast = parser.parse("""def f():
    return
""")
        func_def = ast.statements[0]
        assert isinstance(func_def.body[0], ReturnStatement)
        assert func_def.body[0].value is None


class TestPrintStatement:
    """Tests for print statement parsing."""

    def test_print_string(self):
        """Test print statement with string."""
        parser = PyrlLarkParser()
        ast = parser.parse('print("Hello")')
        assert isinstance(ast.statements[0], PrintStatement)

    def test_print_variable(self):
        """Test print statement with variable."""
        parser = PyrlLarkParser()
        ast = parser.parse("print($x)")
        assert isinstance(ast.statements[0], PrintStatement)


class TestAssertStatement:
    """Tests for assert statement parsing."""

    def test_assert_simple(self):
        """Test simple assert."""
        parser = PyrlLarkParser()
        ast = parser.parse("assert True")
        assert isinstance(ast.statements[0], AssertStatement)

    def test_assert_comparison(self):
        """Test assert with comparison."""
        parser = PyrlLarkParser()
        ast = parser.parse("assert $x == 5")
        assert isinstance(ast.statements[0], AssertStatement)
        # The comparison is inside the left expression as a BinaryOp
        assert isinstance(ast.statements[0].left, BinaryOp)
        assert ast.statements[0].left.operator == '=='


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_parse_lark(self):
        """Test parse_lark convenience function."""
        ast = parse_lark("42")
        assert isinstance(ast, Program)

    def test_get_parser(self):
        """Test get_parser returns same instance."""
        p1 = get_parser()
        p2 = get_parser()
        assert p1 is p2

    def test_get_parser_debug(self):
        """Test get_parser with debug creates new instance."""
        p1 = get_parser()
        p2 = get_parser(debug=True)
        assert p1 is not p2


class TestParseErrors:
    """Tests for parse error handling."""

    def test_invalid_syntax(self):
        """Test invalid syntax raises error."""
        parser = PyrlLarkParser()
        with pytest.raises(SyntaxError):
            parser.parse("def :")

    def test_unclosed_string(self):
        """Test unclosed string raises error."""
        parser = PyrlLarkParser()
        with pytest.raises(SyntaxError):
            parser.parse('"unclosed')

    def test_invalid_variable(self):
        """Test invalid variable syntax."""
        parser = PyrlLarkParser()
        with pytest.raises(SyntaxError):
            parser.parse("$123")
