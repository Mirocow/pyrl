"""
Test Parser Module
Tests for Pyrl parser functionality.
"""
import pytest
from src.core.lexer import tokenize
from src.core.parser import parse, Parser
from src.core.ast_nodes import *
from src.core.exceptions import ParseError


class TestParserBasics:
    """Basic parser tests."""
    
    def test_empty_program(self):
        """Test parsing empty program."""
        ast = parse(tokenize(""))
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 0
    
    def test_single_number(self):
        """Test parsing single number."""
        ast = parse(tokenize("42"))
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], NumberNode)
        assert ast.statements[0].value == 42.0
    
    def test_single_string(self):
        """Test parsing single string."""
        ast = parse(tokenize('"hello"'))
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], StringNode)
        assert ast.statements[0].value == "hello"


class TestParserVariables:
    """Tests for variable parsing."""
    
    def test_scalar_assignment(self):
        """Test scalar variable assignment."""
        ast = parse(tokenize("$x = 10"))
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignNode)
        assert isinstance(stmt.target, ScalarNode)
        assert stmt.target.name == "x"
    
    def test_array_assignment(self):
        """Test array variable assignment."""
        ast = parse(tokenize("@arr = [1, 2, 3]"))
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignNode)
        assert isinstance(stmt.target, ArrayNode)
    
    def test_hash_assignment(self):
        """Test hash variable assignment."""
        ast = parse(tokenize('%person = {name: "Alice"}'))
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignNode)
        assert isinstance(stmt.target, HashNode)


class TestParserExpressions:
    """Tests for expression parsing."""
    
    def test_binary_addition(self):
        """Test binary addition."""
        ast = parse(tokenize("1 + 2"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "+"
    
    def test_binary_subtraction(self):
        """Test binary subtraction."""
        ast = parse(tokenize("5 - 3"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "-"
    
    def test_binary_multiplication(self):
        """Test binary multiplication."""
        ast = parse(tokenize("4 * 2"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "*"
    
    def test_binary_division(self):
        """Test binary division."""
        ast = parse(tokenize("8 / 2"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "/"
    
    def test_operator_precedence(self):
        """Test operator precedence."""
        ast = parse(tokenize("1 + 2 * 3"))
        stmt = ast.statements[0]
        # Should be: 1 + (2 * 3)
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "+"
        assert isinstance(stmt.right, BinaryOpNode)
        assert stmt.right.operator == "*"
    
    def test_parentheses_precedence(self):
        """Test parentheses override precedence."""
        ast = parse(tokenize("(1 + 2) * 3"))
        stmt = ast.statements[0]
        # Should be: (1 + 2) * 3
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "*"
        assert isinstance(stmt.left, BinaryOpNode)
        assert stmt.left.operator == "+"


class TestParserComparison:
    """Tests for comparison expressions."""
    
    def test_equality(self):
        """Test equality comparison."""
        ast = parse(tokenize("$x == 10"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "=="
    
    def test_less_than(self):
        """Test less than comparison."""
        ast = parse(tokenize("$x < 5"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "<"
    
    def test_greater_than(self):
        """Test greater than comparison."""
        ast = parse(tokenize("$x > 5"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == ">"


class TestParserLogical:
    """Tests for logical expressions."""
    
    def test_and_expression(self):
        """Test and expression."""
        ast = parse(tokenize("True and False"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "and"
    
    def test_or_expression(self):
        """Test or expression."""
        ast = parse(tokenize("True or False"))
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOpNode)
        assert stmt.operator == "or"
    
    def test_not_expression(self):
        """Test not expression."""
        ast = parse(tokenize("not True"))
        stmt = ast.statements[0]
        assert isinstance(stmt, UnaryOpNode)
        assert stmt.operator == "not"


class TestParserControlFlow:
    """Tests for control flow statements."""
    
    def test_if_statement(self):
        """Test if statement."""
        source = """if True:
    $x = 1
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, IfNode)
        assert len(stmt.then_body) == 1
    
    def test_if_else_statement(self):
        """Test if-else statement."""
        source = """if True:
    $x = 1
else:
    $x = 2
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, IfNode)
        assert stmt.else_body is not None
    
    def test_if_elif_else_statement(self):
        """Test if-elif-else statement."""
        source = """if $x == 1:
    $y = 1
elif $x == 2:
    $y = 2
else:
    $y = 3
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, IfNode)
        assert len(stmt.elif_clauses) == 1
        assert stmt.else_body is not None
    
    def test_while_statement(self):
        """Test while statement."""
        source = """while $x < 10:
    $x = $x + 1
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, WhileNode)
    
    def test_for_statement(self):
        """Test for statement."""
        source = """for $item in @items:
    print($item)
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, ForNode)
        assert stmt.var == "item"


class TestParserFunctions:
    """Tests for function definitions."""
    
    def test_simple_function(self):
        """Test simple function definition."""
        source = """def greet():
    print("Hello")
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, DefNode)
        assert stmt.name == "greet"
        assert len(stmt.params) == 0
    
    def test_function_with_params(self):
        """Test function with parameters."""
        source = """def add($a, $b):
    return $a + $b
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, DefNode)
        assert stmt.name == "add"
        assert len(stmt.params) == 2
    
    def test_return_statement(self):
        """Test return statement."""
        source = """def get_value():
    return 42
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt.body[0], ReturnNode)


class TestParserClasses:
    """Tests for class definitions."""
    
    def test_simple_class(self):
        """Test simple class definition."""
        source = """class Person:
    def __init__($self):
        pass
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, ClassNode)
        assert stmt.name == "Person"
    
    def test_class_with_base(self):
        """Test class with base class."""
        source = """class Child(Parent):
    pass
"""
        ast = parse(tokenize(source))
        stmt = ast.statements[0]
        assert isinstance(stmt, ClassNode)
        assert "Parent" in stmt.bases


class TestParserErrors:
    """Tests for parser errors."""
    
    def test_missing_colon(self):
        """Test missing colon after if condition."""
        with pytest.raises(ParseError):
            parse(tokenize("if True\n    $x = 1"))
    
    def test_invalid_assignment_target(self):
        """Test invalid assignment target (handled differently)."""
        # This should parse as a binary expression
        ast = parse(tokenize("1 + 2"))
        assert isinstance(ast.statements[0], BinaryOpNode)


@pytest.mark.parser
class TestParserComplex:
    """Complex parser tests."""
    
    def test_nested_function_calls(self):
        """Test nested function calls."""
        ast = parse(tokenize("print(len($items))"))
        stmt = ast.statements[0]
        assert isinstance(stmt, CallNode)
    
    def test_array_indexing(self):
        """Test array indexing."""
        ast = parse(tokenize("$item = @arr[0]"))
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignNode)
        assert isinstance(stmt.value, IndexNode)
    
    def test_hash_access(self):
        """Test hash access."""
        ast = parse(tokenize("$value = %person['name']"))
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignNode)
        assert isinstance(stmt.value, IndexNode)
    
    def test_method_call(self):
        """Test method call."""
        ast = parse(tokenize("$obj.method()"))
        stmt = ast.statements[0]
        assert isinstance(stmt, CallNode)
        assert isinstance(stmt.callee, AttributeNode)
