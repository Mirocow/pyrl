"""
Comprehensive VM Tests for Pyrl
100% coverage tests for VM, builtins, and control flow.
"""
import pytest
import math
import sys
from io import StringIO
from src.core.vm import (
    PyrlVM,
    PyrlFunction,
    Environment,
    PyrlRuntimeError,
    ReturnValue,
    BreakException,
    ContinueException,
    run,
    run_file,
    create_vm,
    BUILTINS,
    CONSTANTS,
)


@pytest.fixture
def vm():
    """Create a fresh VM instance for each test."""
    return PyrlVM()


@pytest.fixture
def debug_vm():
    """Create a debug VM instance."""
    return PyrlVM(debug=True)


class TestVMCreation:
    """Tests for VM creation."""

    def test_create_vm_default(self):
        """Test creating VM with default settings."""
        vm = PyrlVM()
        assert vm is not None
        assert not vm.debug
        assert vm.env is not None
        assert vm.output == []

    def test_create_vm_debug(self):
        """Test creating VM with debug mode."""
        vm = PyrlVM(debug=True)
        assert vm.debug

    def test_create_vm_function(self):
        """Test create_vm convenience function."""
        vm = create_vm()
        assert isinstance(vm, PyrlVM)

    def test_vm_has_builtins(self, vm):
        """Test VM has built-in functions."""
        assert 'print' in vm.env.variables
        assert 'len' in vm.env.variables
        assert 'range' in vm.env.variables

    def test_vm_has_constants(self, vm):
        """Test VM has constants."""
        assert vm.env.get('True') is True
        assert vm.env.get('False') is False
        assert vm.env.get('None') is None
        assert vm.env.get('PI') == math.pi


class TestVMRun:
    """Tests for running code."""

    def test_run_empty(self, vm):
        """Test running empty code."""
        result = vm.run("")
        assert result is None

    def test_run_single_number(self, vm):
        """Test running single number."""
        result = vm.run("42")
        assert result == 42

    def test_run_single_string(self, vm):
        """Test running single string."""
        result = vm.run('"hello"')
        assert result == "hello"

    def test_run_single_boolean(self, vm):
        """Test running single boolean."""
        result = vm.run("True")
        assert result is True

    def test_run_single_none(self, vm):
        """Test running None."""
        result = vm.run("None")
        assert result is None


class TestVariables:
    """Tests for variable handling."""

    def test_scalar_assignment(self, vm):
        """Test scalar variable assignment."""
        vm.run("$x = 10")
        assert vm.get_variable("x") == 10

    def test_scalar_reassignment(self, vm):
        """Test scalar variable reassignment."""
        vm.run("$x = 10")
        vm.run("$x = 20")
        assert vm.get_variable("x") == 20

    def test_array_assignment(self, vm):
        """Test array variable assignment."""
        vm.run("@arr = [1, 2, 3]")
        assert vm.get_variable("arr") == [1, 2, 3]

    def test_hash_assignment(self, vm):
        """Test hash variable assignment."""
        vm.run('%h = {name: "Alice"}')
        h = vm.get_variable("h")
        assert h["name"] == "Alice"

    def test_undefined_variable(self, vm):
        """Test accessing undefined variable raises error."""
        with pytest.raises(PyrlRuntimeError):
            vm.run("$undefined")

    def test_has_variable(self, vm):
        """Test has_variable method."""
        assert not vm.has_variable("x")
        vm.run("$x = 1")
        assert vm.has_variable("x")

    def test_set_get_variable(self, vm):
        """Test set_variable and get_variable methods."""
        vm.set_variable("test", 123)
        assert vm.get_variable("test") == 123


class TestArithmetic:
    """Tests for arithmetic operations."""

    def test_addition(self, vm):
        """Test addition."""
        assert vm.run("1 + 2") == 3
        assert vm.run("0 + 0") == 0
        assert vm.run("-1 + 1") == 0

    def test_subtraction(self, vm):
        """Test subtraction."""
        assert vm.run("5 - 3") == 2
        assert vm.run("0 - 5") == -5

    def test_multiplication(self, vm):
        """Test multiplication."""
        assert vm.run("4 * 3") == 12
        assert vm.run("0 * 100") == 0

    def test_division(self, vm):
        """Test division."""
        assert vm.run("10 / 2") == 5
        assert vm.run("7 / 2") == 3.5

    def test_floor_division(self, vm):
        """Test floor division."""
        assert vm.run("7 // 2") == 3
        assert vm.run("10 // 3") == 3

    def test_modulo(self, vm):
        """Test modulo."""
        assert vm.run("7 % 3") == 1
        assert vm.run("10 % 5") == 0

    def test_operator_precedence(self, vm):
        """Test operator precedence."""
        assert vm.run("2 + 3 * 4") == 14
        assert vm.run("(2 + 3) * 4") == 20

    def test_float_arithmetic(self, vm):
        """Test float arithmetic."""
        assert vm.run("3.14 + 1.86") == pytest.approx(5.0)
        assert vm.run("2.5 * 2") == 5.0


class TestComparison:
    """Tests for comparison operations."""

    def test_equality(self, vm):
        """Test equality."""
        assert vm.run("5 == 5") is True
        assert vm.run("5 == 6") is False
        assert vm.run('"a" == "a"') is True

    def test_inequality(self, vm):
        """Test inequality."""
        assert vm.run("5 != 6") is True
        assert vm.run("5 != 5") is False

    def test_less_than(self, vm):
        """Test less than."""
        assert vm.run("3 < 5") is True
        assert vm.run("5 < 3") is False
        assert vm.run("5 < 5") is False

    def test_less_equal(self, vm):
        """Test less than or equal."""
        assert vm.run("3 <= 5") is True
        assert vm.run("5 <= 5") is True
        assert vm.run("6 <= 5") is False

    def test_greater_than(self, vm):
        """Test greater than."""
        assert vm.run("5 > 3") is True
        assert vm.run("3 > 5") is False

    def test_greater_equal(self, vm):
        """Test greater than or equal."""
        assert vm.run("5 >= 3") is True
        assert vm.run("5 >= 5") is True
        assert vm.run("3 >= 5") is False


class TestLogical:
    """Tests for logical operations."""

    def test_and(self, vm):
        """Test and operator."""
        assert vm.run("True and True") is True
        assert vm.run("True and False") is False
        assert vm.run("False and True") is False
        assert vm.run("False and False") is False

    def test_or(self, vm):
        """Test or operator."""
        assert vm.run("True or True") is True
        assert vm.run("True or False") is True
        assert vm.run("False or True") is True
        assert vm.run("False or False") is False

    def test_not(self, vm):
        """Test not operator."""
        assert vm.run("not True") is False
        assert vm.run("not False") is True
        assert vm.run("!True") is False

    def test_short_circuit_and(self, vm):
        """Test short-circuit evaluation for and."""
        # In Pyrl, assignments must be statements, not expressions
        # So we test with a function call that has side effects
        vm.run("""
$executed = False
def set_executed():
    $executed = True
    return True
""")
        # When left is False, right should not be evaluated
        vm.run("False and set_executed()")
        assert vm.get_variable("executed") is False

    def test_short_circuit_or(self, vm):
        """Test short-circuit evaluation for or."""
        vm.run("""
$executed = False
def set_executed():
    $executed = True
    return True
""")
        # When left is True, right should not be evaluated
        vm.run("True or set_executed()")
        assert vm.get_variable("executed") is False


class TestArrays:
    """Tests for array operations."""

    def test_empty_array(self, vm):
        """Test empty array."""
        assert vm.run("[]") == []

    def test_array_literal(self, vm):
        """Test array literal."""
        assert vm.run("[1, 2, 3]") == [1, 2, 3]

    def test_array_indexing(self, vm):
        """Test array indexing."""
        vm.run("@arr = [10, 20, 30]")
        assert vm.run("@arr[0]") == 10
        assert vm.run("@arr[2]") == 30

    def test_array_assignment(self, vm):
        """Test array element assignment."""
        vm.run("@arr = [1, 2, 3]")
        vm.run("@arr[0] = 100")
        assert vm.get_variable("arr") == [100, 2, 3]

    def test_nested_arrays(self, vm):
        """Test nested arrays."""
        assert vm.run("[[1, 2], [3, 4]]") == [[1, 2], [3, 4]]


class TestHashes:
    """Tests for hash operations."""

    def test_empty_hash(self, vm):
        """Test empty hash."""
        assert vm.run("{}") == {}

    def test_hash_literal(self, vm):
        """Test hash literal."""
        result = vm.run('{name: "Alice", age: 30}')
        assert result["name"] == "Alice"
        assert result["age"] == 30

    def test_hash_access(self, vm):
        """Test hash key access."""
        vm.run('%person = {name: "Bob"}')
        assert vm.run('%person["name"]') == "Bob"

    def test_hash_assignment(self, vm):
        """Test hash key assignment."""
        vm.run("%h = {}")
        vm.run('%h["key"] = "value"')
        assert vm.get_variable("h")["key"] == "value"


class TestControlFlow:
    """Tests for control flow statements."""

    def test_if_true(self, vm):
        """Test if with true condition."""
        vm.run("""
if True:
    $x = 1
""")
        assert vm.get_variable("x") == 1

    def test_if_false(self, vm):
        """Test if with false condition."""
        vm.run("$x = 0")
        vm.run("""
if False:
    $x = 1
""")
        assert vm.get_variable("x") == 0

    def test_if_else(self, vm):
        """Test if-else."""
        vm.run("""
if False:
    $x = 1
else:
    $x = 2
""")
        assert vm.get_variable("x") == 2

    def test_if_elif_else(self, vm):
        """Test if-elif-else."""
        vm.run("""
$x = 2
if $x == 1:
    $y = 1
elif $x == 2:
    $y = 2
else:
    $y = 3
""")
        assert vm.get_variable("y") == 2

    def test_for_loop(self, vm):
        """Test for loop."""
        vm.run("""
$sum = 0
for $i in [1, 2, 3, 4, 5]:
    $sum = $sum + $i
""")
        assert vm.get_variable("sum") == 15

    def test_for_loop_range(self, vm):
        """Test for loop with range."""
        vm.run("""
$sum = 0
for $i in range(5):
    $sum = $sum + $i
""")
        assert vm.get_variable("sum") == 10

    def test_while_loop(self, vm):
        """Test while loop."""
        vm.run("""
$i = 0
while $i < 5:
    $i = $i + 1
""")
        assert vm.get_variable("i") == 5


class TestFunctions:
    """Tests for function definitions and calls."""

    def test_function_definition(self, vm):
        """Test function definition."""
        vm.run("""
def greet():
    return "Hello"
""")
        assert vm.has_variable("greet")
        func = vm.get_variable("greet")
        assert isinstance(func, PyrlFunction)

    def test_function_call(self, vm):
        """Test function call."""
        vm.run("""
def add($a, $b):
    return $a + $b
$result = add(3, 4)
""")
        assert vm.get_variable("result") == 7

    def test_function_no_return(self, vm):
        """Test function with no return statement."""
        vm.run("""
def no_return():
    $x = 1
$result = no_return()
""")
        # Function returns last evaluated value (like Python implicit return)
        # $x = 1 returns 1, so the function returns 1
        assert vm.get_variable("result") == 1

    def test_recursive_function(self, vm):
        """Test recursive function."""
        vm.run("""
def factorial($n):
    if $n <= 1:
        return 1
    return $n * factorial($n - 1)
$result = factorial(5)
""")
        assert vm.get_variable("result") == 120

    def test_fibonacci(self, vm):
        """Test Fibonacci function."""
        vm.run("""
def fib($n):
    if $n <= 1:
        return $n
    return fib($n - 1) + fib($n - 2)
$result = fib(10)
""")
        assert vm.get_variable("result") == 55

    def test_closure(self, vm):
        """Test function closure."""
        vm.run("""
$x = 10
def get_x():
    return $x
$result = get_x()
""")
        assert vm.get_variable("result") == 10


class TestBuiltins:
    """Tests for built-in functions."""

    def test_print(self, vm, capsys):
        """Test print function."""
        vm.run('print("Hello")')
        captured = capsys.readouterr()
        assert "Hello" in captured.out

    def test_len_string(self, vm):
        """Test len with string."""
        assert vm.run('len("hello")') == 5

    def test_len_array(self, vm):
        """Test len with array."""
        vm.run("@arr = [1, 2, 3]")
        assert vm.run("len(@arr)") == 3

    def test_range(self, vm):
        """Test range function."""
        assert vm.run("range(5)") == [0, 1, 2, 3, 4]
        assert vm.run("range(1, 4)") == [1, 2, 3]
        assert vm.run("range(0, 10, 2)") == [0, 2, 4, 6, 8]

    def test_type(self, vm):
        """Test type function."""
        assert vm.run("type(42)") == "int"
        assert vm.run('type("hello")') == "str"
        assert vm.run("type([1, 2])") == "array"
        assert vm.run("type({a: 1})") == "hash"

    def test_int(self, vm):
        """Test int conversion."""
        assert vm.run('int("42")') == 42
        assert vm.run("int(3.7)") == 3

    def test_float(self, vm):
        """Test float conversion."""
        assert vm.run('float("3.14")') == 3.14
        assert vm.run("float(42)") == 42.0

    def test_str(self, vm):
        """Test str conversion."""
        assert vm.run("str(42)") == "42"
        assert vm.run("str(True)") == "True"

    def test_bool(self, vm):
        """Test bool conversion."""
        assert vm.run("bool(1)") is True
        assert vm.run("bool(0)") is False
        assert vm.run('bool("")') is False

    def test_min_max(self, vm):
        """Test min and max functions."""
        assert vm.run("min(1, 2, 3)") == 1
        assert vm.run("max(1, 2, 3)") == 3
        assert vm.run("min([5, 3, 8])") == 3

    def test_sum(self, vm):
        """Test sum function."""
        assert vm.run("sum([1, 2, 3, 4])") == 10

    def test_abs(self, vm):
        """Test abs function."""
        assert vm.run("abs(-5)") == 5
        assert vm.run("abs(5)") == 5

    def test_round(self, vm):
        """Test round function."""
        assert vm.run("round(3.7)") == 4
        assert vm.run("round(3.14159, 2)") == 3.14

    def test_sqrt(self, vm):
        """Test sqrt function."""
        assert vm.run("sqrt(16)") == 4.0

    def test_pow(self, vm):
        """Test pow function."""
        assert vm.run("pow(2, 3)") == 8

    def test_lower_upper(self, vm):
        """Test lower and upper functions."""
        assert vm.run('lower("HELLO")') == "hello"
        assert vm.run('upper("hello")') == "HELLO"

    def test_strip(self, vm):
        """Test strip function."""
        assert vm.run('strip("  hello  ")') == "hello"

    def test_split(self, vm):
        """Test split function."""
        assert vm.run('split("a,b,c", ",")') == ["a", "b", "c"]

    def test_join(self, vm):
        """Test join function."""
        assert vm.run('join("-", ["a", "b", "c"])') == "a-b-c"

    def test_replace(self, vm):
        """Test replace function."""
        assert vm.run('replace("hello world", "world", "there")') == "hello there"

    def test_append(self, vm):
        """Test append function."""
        vm.run("@arr = [1, 2]")
        vm.run("append(@arr, 3)")
        assert vm.get_variable("arr") == [1, 2, 3]

    def test_keys_values(self, vm):
        """Test keys and values functions."""
        vm.run('%h = {a: 1, b: 2}')
        assert sorted(vm.run("keys(%h)")) == ["a", "b"]
        assert sorted(vm.run("values(%h)")) == [1, 2]


class TestEnvironment:
    """Tests for Environment class."""

    def test_define(self):
        """Test defining variable."""
        env = Environment()
        env.define("x", 10)
        assert env.get("x") == 10

    def test_set(self):
        """Test setting variable."""
        env = Environment()
        env.define("x", 10)
        env.set("x", 20)
        assert env.get("x") == 20

    def test_has(self):
        """Test has method."""
        env = Environment()
        assert not env.has("x")
        env.define("x", 10)
        assert env.has("x")

    def test_parent_scope(self):
        """Test parent scope lookup."""
        parent = Environment()
        parent.define("x", 10)
        child = Environment(parent=parent)
        assert child.get("x") == 10

    def test_undefined_raises_error(self):
        """Test undefined variable raises error."""
        env = Environment()
        with pytest.raises(PyrlRuntimeError):
            env.get("undefined")


class TestExceptions:
    """Tests for exception classes."""

    def test_return_value(self):
        """Test ReturnValue exception."""
        ret = ReturnValue(42)
        assert ret.value == 42

    def test_break_exception(self):
        """Test BreakException."""
        with pytest.raises(BreakException):
            raise BreakException()

    def test_continue_exception(self):
        """Test ContinueException."""
        with pytest.raises(ContinueException):
            raise ContinueException()

    def test_runtime_error(self):
        """Test PyrlRuntimeError."""
        err = PyrlRuntimeError("test error")
        assert "test error" in str(err)


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_run_function(self):
        """Test run convenience function."""
        result = run("1 + 2 + 3")
        assert result == 6

    def test_create_vm_function(self):
        """Test create_vm convenience function."""
        vm = create_vm()
        assert isinstance(vm, PyrlVM)


class TestVMReset:
    """Tests for VM reset functionality."""

    def test_reset_clears_variables(self, vm):
        """Test reset clears variables."""
        vm.run("$x = 100")
        assert vm.has_variable("x")
        vm.reset()
        assert not vm.has_variable("x")

    def test_reset_clears_output(self, vm):
        """Test reset clears output."""
        vm.run('print("hello")')
        assert len(vm.output) > 0
        vm.reset()
        assert vm.output == []

    def test_reset_keeps_builtins(self, vm):
        """Test reset keeps built-in functions."""
        vm.reset()
        assert vm.has_variable("print")
        assert vm.has_variable("len")


class TestComplexPrograms:
    """Tests for complex programs."""

    def test_nested_loops(self, vm):
        """Test nested loops."""
        vm.run("""
$sum = 0
for $i in range(3):
    for $j in range(3):
        $sum = $sum + $i + $j
""")
        # i=0: j=0,1,2 -> 0+1+2 = 3
        # i=1: j=0,1,2 -> 1+2+3 = 6
        # i=2: j=0,1,2 -> 2+3+4 = 9
        # Total: 3+6+9 = 18
        assert vm.get_variable("sum") == 18

    def test_function_with_loop(self, vm):
        """Test function with loop."""
        vm.run("""
def sum_to($n):
    $total = 0
    for $i in range($n + 1):
        $total = $total + $i
    return $total
$result = sum_to(10)
""")
        assert vm.get_variable("result") == 55

    def test_higher_order_pattern(self, vm):
        """Test higher-order function pattern."""
        vm.run("""
@nums = [1, 2, 3, 4, 5]
@doubled = []
for $n in @nums:
    append(@doubled, $n * 2)
""")
        assert vm.get_variable("doubled") == [2, 4, 6, 8, 10]
