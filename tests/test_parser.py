# FILE: tests/test_parser.py
"""
Comprehensive tests for PyrlParser
Tests: parsing, preprocessing, error handling
"""

import pytest
from pyrl_vm import (
    PyrlParser, PyrlSyntaxError,
    AssignmentNode, LiteralNode, BinaryOpNode, VariableNode,
    HashLiteralNode, ArrayLiteralNode, ConditionalNode, LoopNode,
    FunctionDefNode, FunctionCallNode, PrintNode, ReturnNode,
    TestBlockNode, AssertionNode, VueGenNode
)


class TestPyrlParser:
    """Test PyrlParser class"""
    
    def test_parser_initialization(self):
        """Test parser can be initialized"""
        parser = PyrlParser()
        assert parser is not None
        assert parser.parser is not None
    
    def test_parse_empty_code(self):
        """Test parsing empty code"""
        parser = PyrlParser()
        tree = parser.parse("")
        assert tree is not None
    
    def test_parse_whitespace_only(self):
        """Test parsing whitespace only"""
        parser = PyrlParser()
        tree = parser.parse("   \n\t\n   ")
        assert tree is not None


class TestScalarParsing:
    """Test scalar variable parsing"""
    
    def test_parse_scalar_string(self):
        """Test parsing scalar string assignment"""
        parser = PyrlParser()
        tree = parser.parse('$name = "hello"')
        assert tree is not None
    
    def test_parse_scalar_number(self):
        """Test parsing scalar number assignment"""
        parser = PyrlParser()
        tree = parser.parse('$age = 25')
        assert tree is not None
    
    def test_parse_scalar_boolean(self):
        """Test parsing scalar boolean assignment"""
        parser = PyrlParser()
        tree = parser.parse('$active = true')
        assert tree is not None
        
        tree = parser.parse('$inactive = false')
        assert tree is not None
    
    def test_parse_scalar_none(self):
        """Test parsing scalar null assignment"""
        parser = PyrlParser()
        tree = parser.parse('$empty = none')
        assert tree is not None
        
        tree = parser.parse('$empty2 = null')
        assert tree is not None


class TestArrayParsing:
    """Test array parsing"""
    
    def test_parse_empty_array(self):
        """Test parsing empty array"""
        parser = PyrlParser()
        tree = parser.parse('@items = []')
        assert tree is not None
    
    def test_parse_array_with_elements(self):
        """Test parsing array with elements"""
        parser = PyrlParser()
        tree = parser.parse('@items = [1, 2, 3]')
        assert tree is not None
    
    def test_parse_array_with_strings(self):
        """Test parsing array with strings"""
        parser = PyrlParser()
        tree = parser.parse('@names = ["Alice", "Bob", "Charlie"]')
        assert tree is not None
    
    def test_parse_array_access(self):
        """Test parsing array access"""
        parser = PyrlParser()
        tree = parser.parse('$first = @items[0]')
        assert tree is not None
    
    def test_parse_array_assignment(self):
        """Test parsing array index assignment"""
        parser = PyrlParser()
        tree = parser.parse('@items[0] = "new value"')
        assert tree is not None


class TestHashParsing:
    """Test hash/dict parsing"""
    
    def test_parse_empty_hash(self):
        """Test parsing empty hash"""
        parser = PyrlParser()
        tree = parser.parse('%data = {}')
        assert tree is not None
    
    def test_parse_hash_with_items(self):
        """Test parsing hash with items"""
        parser = PyrlParser()
        tree = parser.parse('%user = {"name": "Alice", "age": 30}')
        assert tree is not None
    
    def test_parse_hash_access(self):
        """Test parsing hash access"""
        parser = PyrlParser()
        tree = parser.parse('$name = %user["name"]')
        assert tree is not None
    
    def test_parse_hash_assignment(self):
        """Test parsing hash key assignment"""
        parser = PyrlParser()
        tree = parser.parse('%user["email"] = "test@example.com"')
        assert tree is not None
    
    def test_parse_nested_hash(self):
        """Test parsing nested hash"""
        parser = PyrlParser()
        tree = parser.parse('%data = {"outer": {"inner": "value"}}')
        assert tree is not None


class TestFunctionParsing:
    """Test function parsing"""
    
    def test_parse_function_no_params(self):
        """Test parsing function with no parameters"""
        parser = PyrlParser()
        tree = parser.parse('&greet() = { print("Hello") }')
        assert tree is not None
    
    def test_parse_function_with_params(self):
        """Test parsing function with parameters"""
        parser = PyrlParser()
        tree = parser.parse('&add($a, $b) = { return $a + $b }')
        assert tree is not None
    
    def test_parse_function_call(self):
        """Test parsing function call"""
        parser = PyrlParser()
        tree = parser.parse('$result = &add(1, 2)')
        assert tree is not None
    
    def test_parse_function_call_no_args(self):
        """Test parsing function call without arguments"""
        parser = PyrlParser()
        tree = parser.parse('&greet()')
        assert tree is not None


class TestConditionalParsing:
    """Test conditional parsing"""
    
    def test_parse_if_only(self):
        """Test parsing if statement only"""
        parser = PyrlParser()
        tree = parser.parse('if $x > 0 { print("positive") }')
        assert tree is not None
    
    def test_parse_if_else(self):
        """Test parsing if-else statement"""
        parser = PyrlParser()
        tree = parser.parse('if $x > 0 { print("positive") } else { print("non-positive") }')
        assert tree is not None
    
    def test_parse_nested_if(self):
        """Test parsing nested if statements"""
        parser = PyrlParser()
        tree = parser.parse('''
            if $x > 0 {
                if $x > 10 {
                    print("big")
                }
            }
        ''')
        assert tree is not None


class TestLoopParsing:
    """Test loop parsing"""
    
    def test_parse_for_loop(self):
        """Test parsing for loop"""
        parser = PyrlParser()
        tree = parser.parse('for $i in @items { print($i) }')
        assert tree is not None
    
    def test_parse_while_loop(self):
        """Test parsing while loop"""
        parser = PyrlParser()
        tree = parser.parse('while $count < 10 { $count = $count + 1 }')
        assert tree is not None
    
    def test_parse_nested_loops(self):
        """Test parsing nested loops"""
        parser = PyrlParser()
        tree = parser.parse('''
            for $i in @outer {
                for $j in @inner {
                    print($i)
                }
            }
        ''')
        assert tree is not None


class TestRegexParsing:
    """Test regex parsing"""
    
    def test_parse_regex_literal(self):
        """Test parsing regex literal"""
        parser = PyrlParser()
        tree = parser.parse('$pattern = r"^[a-z]+$"')
        assert tree is not None
    
    def test_parse_regex_match(self):
        """Test parsing regex match operation"""
        parser = PyrlParser()
        tree = parser.parse('if $email =~ $pattern { print("valid") }')
        assert tree is not None
    
    def test_parse_regex_not_match(self):
        """Test parsing regex not match operation"""
        parser = PyrlParser()
        tree = parser.parse('if $email !~ $pattern { print("invalid") }')
        assert tree is not None


class TestTestBlockParsing:
    """Test block parsing"""
    
    def test_parse_test_block_no_name(self):
        """Test parsing test block without name"""
        parser = PyrlParser()
        tree = parser.parse('test { assert 1 == 1 }')
        assert tree is not None
    
    def test_parse_test_block_with_name(self):
        """Test parsing test block with name"""
        parser = PyrlParser()
        tree = parser.parse('test "My Test" { assert 1 == 1 }')
        assert tree is not None
    
    def test_parse_multiple_assertions(self):
        """Test parsing multiple assertions in test block"""
        parser = PyrlParser()
        tree = parser.parse('''
            test "Multiple Assertions" {
                assert 1 == 1
                assert 2 > 1
                assert 3 != 4
            }
        ''')
        assert tree is not None


class TestVueParsing:
    """Test Vue component generation parsing"""
    
    def test_parse_vue_component_basic(self):
        """Test parsing basic Vue component"""
        parser = PyrlParser()
        tree = parser.parse('vue "MyComponent" { }')
        assert tree is not None
    
    def test_parse_vue_component_with_props(self):
        """Test parsing Vue component with props"""
        parser = PyrlParser()
        tree = parser.parse('vue "UserCard" { name: "Alice", age: 30 }')
        assert tree is not None


class TestOperatorParsing:
    """Test operator parsing"""
    
    def test_arithmetic_operators(self):
        """Test parsing arithmetic operators"""
        parser = PyrlParser()
        ops = ['+', '-', '*', '/', '%']
        for op in ops:
            tree = parser.parse(f'$result = 10 {op} 5')
            assert tree is not None
    
    def test_comparison_operators(self):
        """Test parsing comparison operators"""
        parser = PyrlParser()
        ops = ['==', '!=', '<', '>', '<=', '>=']
        for op in ops:
            tree = parser.parse(f'if 10 {op} 5 {{ print("test") }}')
            assert tree is not None
    
    def test_logical_operators(self):
        """Test parsing logical operators"""
        parser = PyrlParser()
        tree = parser.parse('if $a && $b { print("both") }')
        assert tree is not None
        
        tree = parser.parse('if $a || $b { print("either") }')
        assert tree is not None
    
    def test_unary_operators(self):
        """Test parsing unary operators"""
        parser = PyrlParser()
        tree = parser.parse('$not_value = !$value')
        assert tree is not None
        
        tree = parser.parse('$negative = -5')
        assert tree is not None


class TestPreprocessing:
    """Test comment removal preprocessing"""
    
    def test_remove_single_line_comment(self):
        """Test removing single line comment"""
        parser = PyrlParser()
        code = '$x = 5 # This is a comment'
        tree = parser.parse(code)
        assert tree is not None
    
    def test_remove_inline_comment(self):
        """Test removing inline comment"""
        parser = PyrlParser()
        code = '$x = 5  # comment after code'
        tree = parser.parse(code)
        assert tree is not None
    
    def test_preserve_comment_in_string(self):
        """Test that # in string is preserved"""
        parser = PyrlParser()
        code = '$str = "hello # world"'
        tree = parser.parse(code)
        assert tree is not None
    
    def test_multiline_with_comments(self):
        """Test multiline code with comments"""
        parser = PyrlParser()
        code = '''
            $x = 5  # set x
            # This is a full line comment
            $y = 10  # set y
        '''
        tree = parser.parse(code)
        assert tree is not None


class TestSyntaxErrors:
    """Test syntax error handling"""
    
    def test_invalid_variable_name(self):
        """Test invalid variable name raises error"""
        parser = PyrlParser()
        with pytest.raises(PyrlSyntaxError):
            parser.parse('x = 5')  # Missing sigil
    
    def test_unclosed_string(self):
        """Test unclosed string raises error"""
        parser = PyrlParser()
        with pytest.raises(PyrlSyntaxError):
            parser.parse('$str = "unclosed')
    
    def test_invalid_assignment_target(self):
        """Test invalid assignment target"""
        parser = PyrlParser()
        with pytest.raises(PyrlSyntaxError):
            parser.parse('5 = $x')
    
    def test_missing_closing_brace(self):
        """Test missing closing brace"""
        parser = PyrlParser()
        with pytest.raises(PyrlSyntaxError):
            parser.parse('if $x > 0 { print($x)')


class TestStringParsing:
    """Test string parsing variations"""
    
    def test_double_quoted_string(self):
        """Test double quoted string"""
        parser = PyrlParser()
        tree = parser.parse('$str = "hello world"')
        assert tree is not None
    
    def test_single_quoted_string(self):
        """Test single quoted string"""
        parser = PyrlParser()
        tree = parser.parse("$str = 'hello world'")
        assert tree is not None
    
    def test_string_with_escape(self):
        """Test string with escape sequences"""
        parser = PyrlParser()
        tree = parser.parse('$str = "hello\\nworld"')
        assert tree is not None
    
    def test_empty_string(self):
        """Test empty string"""
        parser = PyrlParser()
        tree = parser.parse('$str = ""')
        assert tree is not None


class TestNumberParsing:
    """Test number parsing"""
    
    def test_integer(self):
        """Test integer parsing"""
        parser = PyrlParser()
        tree = parser.parse('$int = 42')
        assert tree is not None
    
    def test_negative_integer(self):
        """Test negative integer parsing"""
        parser = PyrlParser()
        tree = parser.parse('$neg = -42')
        assert tree is not None
    
    def test_float(self):
        """Test float parsing"""
        parser = PyrlParser()
        tree = parser.parse('$float = 3.14')
        assert tree is not None
    
    def test_negative_float(self):
        """Test negative float parsing"""
        parser = PyrlParser()
        tree = parser.parse('$neg_float = -3.14')
        assert tree is not None
    
    def test_scientific_notation(self):
        """Test scientific notation"""
        parser = PyrlParser()
        tree = parser.parse('$sci = 1.5e10')
        assert tree is not None


class TestComplexExpressions:
    """Test complex expression parsing"""
    
    def test_nested_parentheses(self):
        """Test nested parentheses"""
        parser = PyrlParser()
        tree = parser.parse('$result = ((1 + 2) * (3 + 4))')
        assert tree is not None
    
    def test_chained_comparisons(self):
        """Test chained method calls style"""
        parser = PyrlParser()
        tree = parser.parse('$result = $a + $b * $c - $d')
        assert tree is not None
    
    def test_complex_condition(self):
        """Test complex condition"""
        parser = PyrlParser()
        tree = parser.parse('if ($a > 0) && ($b < 10) || ($c == 5) { print("complex") }')
        assert tree is not None


class TestReturnStatement:
    """Test return statement parsing"""
    
    def test_return_with_value(self):
        """Test return with value"""
        parser = PyrlParser()
        tree = parser.parse('&func() = { return 42 }')
        assert tree is not None
    
    def test_return_without_value(self):
        """Test return without value"""
        parser = PyrlParser()
        tree = parser.parse('&func() = { return }')
        assert tree is not None
    
    def test_return_variable(self):
        """Test return variable"""
        parser = PyrlParser()
        tree = parser.parse('&func() = { return $result }')
        assert tree is not None


class TestPrintStatement:
    """Test print statement parsing"""
    
    def test_print_literal(self):
        """Test print literal"""
        parser = PyrlParser()
        tree = parser.parse('print("Hello")')
        assert tree is not None
    
    def test_print_variable(self):
        """Test print variable"""
        parser = PyrlParser()
        tree = parser.parse('print($value)')
        assert tree is not None
    
    def test_print_expression(self):
        """Test print expression"""
        parser = PyrlParser()
        tree = parser.parse('print($a + $b)')
        assert tree is not None
