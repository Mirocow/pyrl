"""
Test VM Module
Tests for Pyrl VM functionality.
"""
import pytest
from src.core.vm import PyrlVM, run, create_vm
from src.core.exceptions import RuntimeError, VariableError


class TestVMBasics:
    """Basic VM tests."""
    
    def test_create_vm(self):
        """Test creating a VM instance."""
        vm = PyrlVM()
        assert vm is not None
        assert not vm.debug
    
    def test_create_vm_debug(self):
        """Test creating VM with debug mode."""
        vm = PyrlVM(debug=True)
        assert vm.debug
    
    def test_run_empty(self):
        """Test running empty source."""
        vm = PyrlVM()
        result = vm.run("")
        assert result is None
    
    def test_run_single_number(self):
        """Test running a single number."""
        vm = PyrlVM()
        result = vm.run("42")
        assert result == 42
    
    def test_run_single_string(self):
        """Test running a single string."""
        vm = PyrlVM()
        result = vm.run('"hello"')
        assert result == "hello"


class TestVMVariables:
    """Tests for variable handling."""
    
    def test_scalar_assignment(self, vm):
        """Test scalar variable assignment."""
        vm.run("$x = 10")
        assert vm.get_variable("x") == 10
    
    def test_scalar_retrieval(self, vm):
        """Test scalar variable retrieval."""
        vm.run("$x = 20")
        result = vm.run("$x")
        assert result == 20
    
    def test_multiple_variables(self, vm):
        """Test multiple variables."""
        vm.run("""
$x = 1
$y = 2
$z = $x + $y
""")
        assert vm.get_variable("z") == 3
    
    def test_undefined_variable(self, vm):
        """Test accessing undefined variable raises error."""
        with pytest.raises(VariableError):
            vm.run("$undefined")
    
    def test_variable_update(self, vm):
        """Test updating variable value."""
        vm.run("$x = 1")
        vm.run("$x = 2")
        assert vm.get_variable("x") == 2


class TestVMArithmetic:
    """Tests for arithmetic operations."""
    
    def test_addition(self, vm):
        """Test addition."""
        assert vm.run("1 + 2") == 3
    
    def test_subtraction(self, vm):
        """Test subtraction."""
        assert vm.run("5 - 3") == 2
    
    def test_multiplication(self, vm):
        """Test multiplication."""
        assert vm.run("4 * 3") == 12
    
    def test_division(self, vm):
        """Test division."""
        assert vm.run("10 / 2") == 5
    
    def test_floor_division(self, vm):
        """Test floor division."""
        assert vm.run("7 // 2") == 3
    
    def test_modulo(self, vm):
        """Test modulo."""
        assert vm.run("7 % 3") == 1
    
    def test_power(self, vm):
        """Test power."""
        assert vm.run("2 ** 3") == 8
    
    def test_negative_numbers(self, vm):
        """Test negative numbers."""
        assert vm.run("-5") == -5
        assert vm.run("3 + -2") == 1
    
    def test_float_arithmetic(self, vm):
        """Test float arithmetic."""
        assert vm.run("3.14 + 1.86") == pytest.approx(5.0)


class TestVMComparison:
    """Tests for comparison operations."""
    
    def test_equality(self, vm):
        """Test equality."""
        assert vm.run("5 == 5") is True
        assert vm.run("5 == 6") is False
    
    def test_inequality(self, vm):
        """Test inequality."""
        assert vm.run("5 != 6") is True
        assert vm.run("5 != 5") is False
    
    def test_less_than(self, vm):
        """Test less than."""
        assert vm.run("3 < 5") is True
        assert vm.run("5 < 3") is False
    
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


class TestVMLogical:
    """Tests for logical operations."""
    
    def test_and_true(self, vm):
        """Test and with true operands."""
        assert vm.run("True and True") is True
    
    def test_and_false(self, vm):
        """Test and with false operands."""
        assert vm.run("True and False") is False
        assert vm.run("False and True") is False
    
    def test_or_true(self, vm):
        """Test or with true operands."""
        assert vm.run("True or False") is True
        assert vm.run("False or True") is True
    
    def test_or_false(self, vm):
        """Test or with false operands."""
        assert vm.run("False or False") is False
    
    def test_not(self, vm):
        """Test not."""
        assert vm.run("not True") is False
        assert vm.run("not False") is True


class TestVMControlFlow:
    """Tests for control flow."""
    
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
    
    def test_while_loop(self, vm):
        """Test while loop."""
        vm.run("""
$i = 0
while $i < 5:
    $i = $i + 1
""")
        assert vm.get_variable("i") == 5
    
    def test_for_loop(self, vm):
        """Test for loop."""
        vm.run("""
$sum = 0
for $i in range(5):
    $sum = $sum + $i
""")
        assert vm.get_variable("sum") == 10


class TestVMFunctions:
    """Tests for function definitions and calls."""
    
    def test_function_definition(self, vm):
        """Test function definition."""
        vm.run("""
def greet():
    return "Hello"
""")
        assert vm.has_variable("greet")
    
    def test_function_call(self, vm):
        """Test function call."""
        vm.run("""
def add($a, $b):
    return $a + $b
$result = add(3, 4)
""")
        assert vm.get_variable("result") == 7
    
    def test_function_with_no_return(self, vm):
        """Test function with no return statement."""
        vm.run("""
def no_return():
    $x = 1
$result = no_return()
""")
        assert vm.get_variable("result") is None


class TestVMArrays:
    """Tests for array operations."""
    
    def test_array_literal(self, vm):
        """Test array literal."""
        vm.run("@arr = [1, 2, 3]")
        assert vm.get_variable("arr") == [1, 2, 3]
    
    def test_array_indexing(self, vm):
        """Test array indexing."""
        vm.run("@arr = [10, 20, 30]")
        assert vm.run("@arr[0]") == 10
        assert vm.run("@arr[2]") == 30
    
    def test_array_length(self, vm):
        """Test array length."""
        vm.run("@arr = [1, 2, 3, 4, 5]")
        assert vm.run("len(@arr)") == 5


class TestVMHashes:
    """Tests for hash/dict operations."""
    
    def test_hash_literal(self, vm):
        """Test hash literal."""
        vm.run('%person = {name: "Alice", age: 30}')
        person = vm.get_variable("person")
        assert person["name"] == "Alice"
        assert person["age"] == 30
    
    def test_hash_access(self, vm):
        """Test hash access."""
        vm.run('%person = {name: "Bob"}')
        assert vm.run('%person["name"]') == "Bob"


class TestVMBuiltins:
    """Tests for built-in functions."""
    
    def test_print(self, vm, capsys):
        """Test print function."""
        vm.run('print("Hello, World!")')
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out
    
    def test_len(self, vm):
        """Test len function."""
        assert vm.run('len("hello")') == 5
        vm.run("@arr = [1, 2, 3]")
        assert vm.run("len(@arr)") == 3
    
    def test_range(self, vm):
        """Test range function."""
        result = vm.run("range(5)")
        assert result == [0, 1, 2, 3, 4]
    
    def test_type(self, vm):
        """Test type function."""
        assert vm.run("type(42)") == "int"
        assert vm.run('type("hello")') == "str"
        assert vm.run("type([1, 2])") == "array"


class TestVMUtility:
    """Tests for VM utility methods."""
    
    def test_set_get_variable(self, vm):
        """Test set_variable and get_variable methods."""
        vm.set_variable("test_var", 123)
        assert vm.get_variable("test_var") == 123
    
    def test_has_variable(self, vm):
        """Test has_variable method."""
        assert not vm.has_variable("nonexistent")
        vm.run("$x = 1")
        assert vm.has_variable("x")
    
    def test_reset(self, vm):
        """Test reset method."""
        vm.run("$x = 100")
        assert vm.has_variable("x")
        vm.reset()
        assert not vm.has_variable("x")
    
    def test_get_globals(self, vm):
        """Test get_globals method."""
        vm.run("$x = 1")
        vm.run("$y = 2")
        globals_dict = vm.get_globals()
        assert "x" in globals_dict
        assert "y" in globals_dict


@pytest.mark.vm
class TestVMComplex:
    """Complex VM tests."""
    
    def test_fibonacci(self, vm):
        """Test Fibonacci sequence calculation."""
        vm.run("""
def fib($n):
    if $n <= 1:
        return $n
    return fib($n - 1) + fib($n - 2)
$result = fib(10)
""")
        assert vm.get_variable("result") == 55
    
    def test_factorial(self, vm):
        """Test factorial calculation."""
        vm.run("""
def factorial($n):
    if $n <= 1:
        return 1
    return $n * factorial($n - 1)
$result = factorial(5)
""")
        assert vm.get_variable("result") == 120
    
    def test_nested_loops(self, vm):
        """Test nested loops."""
        vm.run("""
$sum = 0
for $i in range(3):
    for $j in range(3):
        $sum = $sum + $i + $j
""")
        assert vm.get_variable("sum") == 9


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_run_function(self):
        """Test run convenience function."""
        result = run("1 + 2 + 3")
        assert result == 6
    
    def test_create_vm_function(self):
        """Test create_vm convenience function."""
        vm = create_vm(debug=True)
        assert isinstance(vm, PyrlVM)
        assert vm.debug
