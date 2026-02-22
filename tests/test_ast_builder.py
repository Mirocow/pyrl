# FILE: tests/test_ast_builder.py
"""
Comprehensive tests for ASTBuilder
Tests: AST node creation from parse tree
"""

import pytest
from pyrl_vm import (
    PyrlParser, ASTBuilder,
    ProgramNode, AssignmentNode, BinaryOpNode, UnaryOpNode,
    VariableNode, LiteralNode, HashLiteralNode, ArrayLiteralNode,
    HashAccessNode, ArrayAccessNode, ConditionalNode, LoopNode,
    FunctionDefNode, FunctionCallNode, PrintNode, ReturnNode,
    AssertionNode, TestBlockNode, VueGenNode
)


class TestASTBuilder:
    """Test ASTBuilder class"""
    
    @pytest.fixture
    def parser_builder(self):
        """Create parser and builder"""
        parser = PyrlParser()
        builder = ASTBuilder()
        return parser, builder
    
    def parse_and_build(self, code, parser, builder):
        """Helper to parse and build AST"""
        tree = parser.parse(code)
        return builder.transform(tree)


class TestScalarAST(TestASTBuilder):
    """Test scalar variable AST nodes"""
    
    def test_scalar_string_ast(self, parser_builder):
        """Test scalar string AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$name = "hello"', parser, builder)
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentNode)
        assert stmt.target == '$name'
        assert stmt.target_type == 'scalar'
        assert isinstance(stmt.value, LiteralNode)
        assert stmt.value.value == 'hello'
    
    def test_scalar_number_ast(self, parser_builder):
        """Test scalar number AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$age = 25', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentNode)
        assert stmt.value.value == 25
    
    def test_scalar_boolean_ast(self, parser_builder):
        """Test scalar boolean AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$active = true', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, LiteralNode)
        assert stmt.value.value == True
    
    def test_scalar_none_ast(self, parser_builder):
        """Test scalar null AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$empty = none', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, LiteralNode)
        assert stmt.value.value is None


class TestArrayAST(TestASTBuilder):
    """Test array AST nodes"""
    
    def test_empty_array_ast(self, parser_builder):
        """Test empty array AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('@items = []', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentNode)
        assert stmt.target == '@items'
        assert isinstance(stmt.value, ArrayLiteralNode)
        assert len(stmt.value.items) == 0
    
    def test_array_with_elements_ast(self, parser_builder):
        """Test array with elements AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('@nums = [1, 2, 3]', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, ArrayLiteralNode)
        assert len(stmt.value.items) == 3
    
    def test_array_access_ast(self, parser_builder):
        """Test array access AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$first = @items[0]', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, ArrayAccessNode)
        assert stmt.value.var_name == '@items'


class TestHashAST(TestASTBuilder):
    """Test hash AST nodes"""
    
    def test_empty_hash_ast(self, parser_builder):
        """Test empty hash AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('%data = {}', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentNode)
        assert stmt.target == '%data'
        assert isinstance(stmt.value, HashLiteralNode)
        assert len(stmt.value.items) == 0
    
    def test_hash_with_items_ast(self, parser_builder):
        """Test hash with items AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('%user = {"name": "Alice", "age": 30}', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, HashLiteralNode)
        assert len(stmt.value.items) == 2
    
    def test_hash_access_ast(self, parser_builder):
        """Test hash access AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$name = %user["name"]', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, HashAccessNode)
        assert stmt.value.var_name == '%user'


class TestFunctionAST(TestASTBuilder):
    """Test function AST nodes"""
    
    def test_function_def_ast(self, parser_builder):
        """Test function definition AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('&add($a, $b) = { return $a + $b }', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionDefNode)
        assert stmt.name == '&add'
        assert len(stmt.params) == 2
        assert '$a' in stmt.params
        assert '$b' in stmt.params
    
    def test_function_call_ast(self, parser_builder):
        """Test function call AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$result = &add(1, 2)', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, FunctionCallNode)
        assert stmt.value.name == '&add'
        assert len(stmt.value.args) == 2


class TestConditionalAST(TestASTBuilder):
    """Test conditional AST nodes"""
    
    def test_if_ast(self, parser_builder):
        """Test if statement AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('if $x > 0 { print($x) }', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, ConditionalNode)
        assert stmt.condition is not None
        assert stmt.if_block is not None
        assert stmt.else_block is None
    
    def test_if_else_ast(self, parser_builder):
        """Test if-else statement AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('if $x > 0 { print("pos") } else { print("neg") }', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, ConditionalNode)
        assert stmt.else_block is not None


class TestLoopAST(TestASTBuilder):
    """Test loop AST nodes"""
    
    def test_for_loop_ast(self, parser_builder):
        """Test for loop AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('for $i in @items { print($i) }', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, LoopNode)
        assert stmt.loop_type == 'for'
        assert stmt.var_name == '$i'
        assert stmt.body is not None
    
    def test_while_loop_ast(self, parser_builder):
        """Test while loop AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('while $x < 10 { $x = $x + 1 }', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, LoopNode)
        assert stmt.loop_type == 'while'
        assert stmt.condition is not None


class TestBinaryOpAST(TestASTBuilder):
    """Test binary operation AST nodes"""
    
    def test_addition_ast(self, parser_builder):
        """Test addition AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$sum = 1 + 2', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, BinaryOpNode)
        assert stmt.value.op == '+'
    
    def test_multiplication_ast(self, parser_builder):
        """Test multiplication AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$product = 3 * 4', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, BinaryOpNode)
        assert stmt.value.op == '*'
    
    def test_comparison_ast(self, parser_builder):
        """Test comparison AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$equal = $a == $b', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, BinaryOpNode)
        assert stmt.value.op == '=='


class TestUnaryOpAST(TestASTBuilder):
    """Test unary operation AST nodes"""
    
    def test_not_ast(self, parser_builder):
        """Test NOT operation AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$inverse = !$value', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, UnaryOpNode)
        assert stmt.value.op == '!'
    
    def test_negation_ast(self, parser_builder):
        """Test negation AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$negative = -5', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, UnaryOpNode)
        assert stmt.value.op == '-'


class TestAssertionAST(TestASTBuilder):
    """Test assertion AST nodes"""
    
    def test_assertion_equality_ast(self, parser_builder):
        """Test equality assertion AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('assert $x == 5', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, AssertionNode)
        assert stmt.op == '=='
    
    def test_assertion_single_expr_ast(self, parser_builder):
        """Test single expression assertion AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('assert $value', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, AssertionNode)
        assert stmt.op is None


class TestTestBlockAST(TestASTBuilder):
    """Test test block AST nodes"""
    
    def test_test_block_ast(self, parser_builder):
        """Test test block AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('test "MyTest" { assert 1 == 1 }', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, TestBlockNode)
        assert stmt.name == 'MyTest'
        assert len(stmt.statements) == 1


class TestVueAST(TestASTBuilder):
    """Test Vue component AST nodes"""
    
    def test_vue_component_ast(self, parser_builder):
        """Test Vue component AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('vue "Card" { title: "Hello" }', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, VueGenNode)
        assert stmt.name == 'Card'
        assert 'title' in stmt.props


class TestPrintAST(TestASTBuilder):
    """Test print statement AST nodes"""
    
    def test_print_ast(self, parser_builder):
        """Test print statement AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('print("Hello")', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, PrintNode)
        assert isinstance(stmt.value, LiteralNode)
        assert stmt.value.value == 'Hello'


class TestReturnAST(TestASTBuilder):
    """Test return statement AST nodes"""
    
    def test_return_with_value_ast(self, parser_builder):
        """Test return with value AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('return 42', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, ReturnNode)
        assert stmt.value is not None
    
    def test_return_without_value_ast(self, parser_builder):
        """Test return without value AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('return', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, ReturnNode)
        assert stmt.value is None


class TestComplexAST(TestASTBuilder):
    """Test complex expression AST nodes"""
    
    def test_nested_expressions_ast(self, parser_builder):
        """Test nested expressions AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$result = (1 + 2) * (3 + 4)', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, BinaryOpNode)
        assert stmt.value.op == '*'
    
    def test_chained_operations_ast(self, parser_builder):
        """Test chained operations AST"""
        parser, builder = parser_builder
        ast = self.parse_and_build('$result = $a + $b - $c * $d', parser, builder)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, BinaryOpNode)


class TestLiteralValues:
    """Test literal value extraction"""
    
    def test_string_literal_double_quote(self):
        """Test double quoted string literal"""
        builder = ASTBuilder()
        result = builder.STRING('"hello world"')
        assert result == 'hello world'
    
    def test_string_literal_single_quote(self):
        """Test single quoted string literal"""
        builder = ASTBuilder()
        result = builder.STRING("'hello world'")
        assert result == 'hello world'
    
    def test_number_literal_int(self):
        """Test integer literal"""
        builder = ASTBuilder()
        result = builder.NUMBER('42')
        assert result == 42
        assert isinstance(result, int)
    
    def test_number_literal_float(self):
        """Test float literal"""
        builder = ASTBuilder()
        result = builder.NUMBER('3.14')
        assert result == 3.14
        assert isinstance(result, float)
    
    def test_boolean_literal_true(self):
        """Test boolean true literal"""
        builder = ASTBuilder()
        result = builder.BOOLEAN('true')
        assert result == True
    
    def test_boolean_literal_false(self):
        """Test boolean false literal"""
        builder = ASTBuilder()
        result = builder.BOOLEAN('false')
        assert result == False
    
    def test_none_literal(self):
        """Test none literal"""
        builder = ASTBuilder()
        result = builder.NONE('none')
        assert result is None
