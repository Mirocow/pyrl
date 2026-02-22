# FILE: tests/test_interpreter.py
"""
Comprehensive tests for PyrlInterpreter
Tests: execution of all AST node types
"""

import pytest
from pyrl_vm import (
    PyrlVM, PyrlInterpreter, PyrlRuntimeError, PyrlTypeError, ReturnException,
    AssignmentNode, BinaryOpNode, UnaryOpNode, VariableNode, LiteralNode,
    HashLiteralNode, ArrayLiteralNode, HashAccessNode, ArrayAccessNode,
    ConditionalNode, LoopNode, FunctionDefNode, FunctionCallNode,
    PrintNode, ReturnNode, AssertionNode, TestBlockNode, VueGenNode,
    ProgramNode, TestResult
)


class TestInterpreterBasics:
    """Test basic interpreter functionality"""
    
    def test_interpreter_initialization(self):
        """Test interpreter can be initialized"""
        vm = PyrlVM()
        interpreter = PyrlInterpreter(vm)
        assert interpreter is not None
        assert interpreter.vm == vm
    
    def test_execute_none_node(self):
        """Test executing None node"""
        vm = PyrlVM()
        interpreter = PyrlInterpreter(vm)
        result = interpreter.execute(None)
        assert result is None


class TestScalarExecution:
    """Test scalar variable execution"""
    
    def test_execute_scalar_string(self):
        """Test executing scalar string assignment"""
        vm = PyrlVM()
        vm.execute('$name = "Alice"')
        assert vm.get_variable('$name') == 'Alice'
    
    def test_execute_scalar_number(self):
        """Test executing scalar number assignment"""
        vm = PyrlVM()
        vm.execute('$age = 25')
        assert vm.get_variable('$age') == 25
    
    def test_execute_scalar_boolean(self):
        """Test executing scalar boolean assignment"""
        vm = PyrlVM()
        vm.execute('$active = true')
        assert vm.get_variable('$active') == True
        
        vm.execute('$inactive = false')
        assert vm.get_variable('$inactive') == False
    
    def test_execute_scalar_none(self):
        """Test executing scalar null assignment"""
        vm = PyrlVM()
        vm.execute('$empty = none')
        assert vm.get_variable('$empty') is None


class TestArrayExecution:
    """Test array execution"""
    
    def test_execute_empty_array(self):
        """Test executing empty array"""
        vm = PyrlVM()
        vm.execute('@items = []')
        assert vm.get_variable('@items') == []
    
    def test_execute_array_with_elements(self):
        """Test executing array with elements"""
        vm = PyrlVM()
        vm.execute('@nums = [1, 2, 3]')
        assert vm.get_variable('@nums') == [1, 2, 3]
    
    def test_execute_array_access(self):
        """Test executing array access"""
        vm = PyrlVM()
        vm.execute('@items = [10, 20, 30]')
        vm.execute('$first = @items[0]')
        assert vm.get_variable('$first') == 10
    
    def test_execute_array_assignment(self):
        """Test executing array index assignment"""
        vm = PyrlVM()
        vm.execute('@items = [1, 2, 3]')
        vm.execute('@items[0] = 100')
        assert vm.get_variable('@items') == [100, 2, 3]


class TestHashExecution:
    """Test hash execution"""
    
    def test_execute_empty_hash(self):
        """Test executing empty hash"""
        vm = PyrlVM()
        vm.execute('%data = {}')
        assert vm.get_variable('%data') == {}
    
    def test_execute_hash_with_items(self):
        """Test executing hash with items"""
        vm = PyrlVM()
        vm.execute('%user = {"name": "Alice", "age": 30}')
        user = vm.get_variable('%user')
        assert user['name'] == 'Alice'
        assert user['age'] == 30
    
    def test_execute_hash_access(self):
        """Test executing hash access"""
        vm = PyrlVM()
        vm.execute('%user = {"name": "Alice"}')
        vm.execute('$name = %user["name"]')
        assert vm.get_variable('$name') == 'Alice'
    
    def test_execute_hash_assignment(self):
        """Test executing hash key assignment"""
        vm = PyrlVM()
        vm.execute('%user = {}')
        vm.execute('%user["email"] = "test@example.com"')
        assert vm.get_variable('%user')['email'] == 'test@example.com'


class TestBinaryOperations:
    """Test binary operation execution"""
    
    def test_addition(self):
        """Test addition"""
        vm = PyrlVM()
        vm.execute('$sum = 5 + 3')
        assert vm.get_variable('$sum') == 8
    
    def test_subtraction(self):
        """Test subtraction"""
        vm = PyrlVM()
        vm.execute('$diff = 10 - 4')
        assert vm.get_variable('$diff') == 6
    
    def test_multiplication(self):
        """Test multiplication"""
        vm = PyrlVM()
        vm.execute('$product = 6 * 7')
        assert vm.get_variable('$product') == 42
    
    def test_division(self):
        """Test division"""
        vm = PyrlVM()
        vm.execute('$quotient = 20 / 4')
        assert vm.get_variable('$quotient') == 5.0
    
    def test_modulo(self):
        """Test modulo"""
        vm = PyrlVM()
        vm.execute('$remainder = 17 % 5')
        assert vm.get_variable('$remainder') == 2
    
    def test_string_concatenation(self):
        """Test string concatenation"""
        vm = PyrlVM()
        vm.execute('$greeting = "Hello" + " " + "World"')
        assert vm.get_variable('$greeting') == 'Hello World'
    
    def test_division_by_zero(self):
        """Test division by zero raises error"""
        vm = PyrlVM()
        with pytest.raises(PyrlRuntimeError):
            vm.execute('$error = 10 / 0')
    
    def test_modulo_by_zero(self):
        """Test modulo by zero raises error"""
        vm = PyrlVM()
        with pytest.raises(PyrlRuntimeError):
            vm.execute('$error = 10 % 0')


class TestComparisonOperations:
    """Test comparison operation execution"""
    
    def test_equality_true(self):
        """Test equality true"""
        vm = PyrlVM()
        vm.execute('$equal = 5 == 5')
        assert vm.get_variable('$equal') == True
    
    def test_equality_false(self):
        """Test equality false"""
        vm = PyrlVM()
        vm.execute('$equal = 5 == 6')
        assert vm.get_variable('$equal') == False
    
    def test_inequality(self):
        """Test inequality"""
        vm = PyrlVM()
        vm.execute('$neq = 5 != 6')
        assert vm.get_variable('$neq') == True
    
    def test_less_than(self):
        """Test less than"""
        vm = PyrlVM()
        vm.execute('$lt = 3 < 5')
        assert vm.get_variable('$lt') == True
    
    def test_greater_than(self):
        """Test greater than"""
        vm = PyrlVM()
        vm.execute('$gt = 5 > 3')
        assert vm.get_variable('$gt') == True
    
    def test_less_than_equal(self):
        """Test less than or equal"""
        vm = PyrlVM()
        vm.execute('$lte = 5 <= 5')
        assert vm.get_variable('$lte') == True
    
    def test_greater_than_equal(self):
        """Test greater than or equal"""
        vm = PyrlVM()
        vm.execute('$gte = 5 >= 5')
        assert vm.get_variable('$gte') == True


class TestRegexOperations:
    """Test regex operation execution"""
    
    def test_regex_match_true(self):
        """Test regex match returns true"""
        vm = PyrlVM()
        vm.execute('$pattern = r"^[a-z]+$"')
        vm.execute('$match = "hello" =~ $pattern')
        assert vm.get_variable('$match') == True
    
    def test_regex_match_false(self):
        """Test regex match returns false"""
        vm = PyrlVM()
        vm.execute('$pattern = r"^[a-z]+$"')
        vm.execute('$match = "Hello123" =~ $pattern')
        assert vm.get_variable('$match') == False
    
    def test_regex_not_match(self):
        """Test regex not match"""
        vm = PyrlVM()
        vm.execute('$pattern = r"^[a-z]+$"')
        vm.execute('$not_match = "123" !~ $pattern')
        assert vm.get_variable('$not_match') == True


class TestLogicalOperations:
    """Test logical operation execution"""
    
    def test_and_true(self):
        """Test AND true"""
        vm = PyrlVM()
        vm.execute('$and = true && true')
        assert vm.get_variable('$and') == True
    
    def test_and_false(self):
        """Test AND false"""
        vm = PyrlVM()
        vm.execute('$and = true && false')
        assert vm.get_variable('$and') == False
    
    def test_or_true(self):
        """Test OR true"""
        vm = PyrlVM()
        vm.execute('$or = false || true')
        assert vm.get_variable('$or') == True
    
    def test_or_false(self):
        """Test OR false"""
        vm = PyrlVM()
        vm.execute('$or = false && false')
        assert vm.get_variable('$or') == False


class TestUnaryOperations:
    """Test unary operation execution"""
    
    def test_not_true(self):
        """Test NOT true"""
        vm = PyrlVM()
        vm.execute('$not = !true')
        assert vm.get_variable('$not') == False
    
    def test_not_false(self):
        """Test NOT false"""
        vm = PyrlVM()
        vm.execute('$not = !false')
        assert vm.get_variable('$not') == True
    
    def test_negation(self):
        """Test negation"""
        vm = PyrlVM()
        vm.execute('$neg = -42')
        assert vm.get_variable('$neg') == -42


class TestConditionals:
    """Test conditional execution"""
    
    def test_if_true(self, capsys):
        """Test if with true condition"""
        vm = PyrlVM()
        vm.execute('if 1 == 1 { print("yes") }')
        captured = capsys.readouterr()
        assert 'yes' in captured.out
    
    def test_if_false(self, capsys):
        """Test if with false condition"""
        vm = PyrlVM()
        vm.execute('if 1 == 2 { print("yes") }')
        captured = capsys.readouterr()
        assert 'yes' not in captured.out
    
    def test_if_else_true_branch(self, capsys):
        """Test if-else true branch"""
        vm = PyrlVM()
        vm.execute('if 1 == 1 { print("if") } else { print("else") }')
        captured = capsys.readouterr()
        assert 'if' in captured.out
        assert 'else' not in captured.out
    
    def test_if_else_false_branch(self, capsys):
        """Test if-else false branch"""
        vm = PyrlVM()
        vm.execute('if 1 == 2 { print("if") } else { print("else") }')
        captured = capsys.readouterr()
        assert 'if' not in captured.out
        assert 'else' in captured.out


class TestLoops:
    """Test loop execution"""
    
    def test_for_loop(self, capsys):
        """Test for loop"""
        vm = PyrlVM()
        vm.execute('@items = [1, 2, 3]')
        vm.execute('for $i in @items { print($i) }')
        captured = capsys.readouterr()
        assert '1' in captured.out
        assert '2' in captured.out
        assert '3' in captured.out
    
    def test_for_loop_accumulator(self):
        """Test for loop with accumulator"""
        vm = PyrlVM()
        vm.execute('@nums = [1, 2, 3, 4, 5]')
        vm.execute('$sum = 0')
        vm.execute('for $n in @nums { $sum = $sum + $n }')
        assert vm.get_variable('$sum') == 15
    
    def test_while_loop(self):
        """Test while loop"""
        vm = PyrlVM()
        vm.execute('$count = 0')
        vm.execute('while $count < 5 { $count = $count + 1 }')
        assert vm.get_variable('$count') == 5
    
    def test_while_loop_max_iterations(self):
        """Test while loop max iterations"""
        vm = PyrlVM()
        with pytest.raises(PyrlRuntimeError):
            vm.execute('while true { $x = 1 }')


class TestFunctions:
    """Test function execution"""
    
    def test_function_no_params(self):
        """Test function without parameters"""
        vm = PyrlVM()
        vm.execute('&greet() = { return "Hello" }')
        vm.execute('$msg = &greet()')
        assert vm.get_variable('$msg') == 'Hello'
    
    def test_function_with_params(self):
        """Test function with parameters"""
        vm = PyrlVM()
        vm.execute('&add($a, $b) = { return $a + $b }')
        vm.execute('$sum = &add(5, 3)')
        assert vm.get_variable('$sum') == 8
    
    def test_function_no_return(self):
        """Test function without return"""
        vm = PyrlVM()
        vm.execute('&noReturn() = { $x = 5 }')
        vm.execute('$result = &noReturn()')
        assert vm.get_variable('$result') is None
    
    def test_function_not_found(self):
        """Test function not found error"""
        vm = PyrlVM()
        with pytest.raises(PyrlRuntimeError):
            vm.execute('&nonexistent()')


class TestTestBlocks:
    """Test test block execution"""
    
    def test_test_block_success(self):
        """Test successful test block"""
        vm = PyrlVM()
        vm.run_tests('test "Math" { assert 1 + 1 == 2 }')
        summary = vm.get_test_summary()
        assert summary['passed'] == 1
        assert summary['failed'] == 0
    
    def test_test_block_failure(self):
        """Test failed test block"""
        vm = PyrlVM()
        vm.run_tests('test "Fail" { assert 1 == 2 }')
        summary = vm.get_test_summary()
        assert summary['passed'] == 0
        assert summary['failed'] == 1
    
    def test_multiple_assertions(self):
        """Test multiple assertions"""
        vm = PyrlVM()
        vm.run_tests('''
            test "Multiple" {
                assert 1 == 1
                assert 2 == 2
                assert 3 == 3
            }
        ''')
        summary = vm.get_test_summary()
        assert summary['passed'] == 3


class TestVueGeneration:
    """Test Vue component generation"""
    
    def test_vue_basic(self):
        """Test basic Vue component"""
        vm = PyrlVM()
        result = vm.execute('vue "Card" { }')
        assert '<template>' in result
        assert 'Card' in result
        assert '<script setup>' in result
    
    def test_vue_with_props(self):
        """Test Vue component with props"""
        vm = PyrlVM()
        result = vm.execute('vue "User" { name: "Alice", age: 30 }')
        assert 'name' in result
        assert 'Alice' in result


class TestPrintStatement:
    """Test print statement execution"""
    
    def test_print_string(self, capsys):
        """Test print string"""
        vm = PyrlVM()
        vm.execute('print("Hello, World!")')
        captured = capsys.readouterr()
        assert 'Hello, World!' in captured.out
    
    def test_print_variable(self, capsys):
        """Test print variable"""
        vm = PyrlVM()
        vm.execute('$msg = "Test"')
        vm.execute('print($msg)')
        captured = capsys.readouterr()
        assert 'Test' in captured.out
    
    def test_print_expression(self, capsys):
        """Test print expression"""
        vm = PyrlVM()
        vm.execute('print(5 + 5)')
        captured = capsys.readouterr()
        assert '10' in captured.out


class TestErrorHandling:
    """Test error handling"""
    
    def test_type_error_hash_access(self):
        """Test type error on hash access"""
        vm = PyrlVM()
        vm.execute('$not_hash = 5')
        with pytest.raises(PyrlTypeError):
            vm.execute('$val = %not_hash["key"]')
    
    def test_type_error_array_access(self):
        """Test type error on array access"""
        vm = PyrlVM()
        vm.execute('$not_array = 5')
        with pytest.raises(PyrlTypeError):
            vm.execute('$val = @not_array[0]')
    
    def test_iterate_non_iterable(self):
        """Test iterate over non-iterable"""
        vm = PyrlVM()
        vm.execute('$not_iterable = 5')
        with pytest.raises(PyrlRuntimeError):
            vm.execute('for $x in $not_iterable { print($x) }')


class TestArrayIndexOperations:
    """Test array index operations"""
    
    def test_array_auto_extend(self):
        """Test array auto extends on assignment"""
        vm = PyrlVM()
        vm.execute('@arr = []')
        vm.execute('@arr[5] = "value"')
        arr = vm.get_variable('@arr')
        assert len(arr) == 6
        assert arr[5] == 'value'
    
    def test_array_out_of_bounds(self):
        """Test array out of bounds returns None"""
        vm = PyrlVM()
        vm.execute('@arr = [1, 2, 3]')
        vm.execute('$val = @arr[100]')
        assert vm.get_variable('$val') is None


class TestComplexExecution:
    """Test complex execution scenarios"""
    
    def test_factorial(self):
        """Test factorial function"""
        vm = PyrlVM()
        vm.execute('''
            &factorial($n) = {
                if $n <= 1 {
                    return 1
                }
                return $n * &factorial($n - 1)
            }
        ''')
        vm.execute('$fact5 = &factorial(5)')
        assert vm.get_variable('$fact5') == 120
    
    def test_fibonacci(self):
        """Test Fibonacci function"""
        vm = PyrlVM()
        vm.execute('''
            &fib($n) = {
                if $n <= 0 {
                    return 0
                }
                if $n == 1 {
                    return 1
                }
                return &fib($n - 1) + &fib($n - 2)
            }
        ''')
        vm.execute('$fib10 = &fib(10)')
        assert vm.get_variable('$fib10') == 55
    
    def test_nested_loops(self):
        """Test nested loops"""
        vm = PyrlVM()
        vm.execute('''
            @matrix = []
            for $i in &range(3) {
                @row = []
                for $j in &range(3) {
                    &push(@row, $i * 3 + $j)
                }
                &push(@matrix, @row)
            }
        ''')
        matrix = vm.get_variable('@matrix')
        assert len(matrix) == 3
