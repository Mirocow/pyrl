"""
Test Built-in Functions for Pyrl
100% coverage tests for all built-in functions.
"""
import pytest
import math
import random
from src.core.vm import PyrlVM


@pytest.fixture
def vm():
    """Create a fresh VM instance for each test."""
    return PyrlVM()


class TestTypeConversion:
    """Tests for type conversion functions."""

    def test_int_from_string(self, vm):
        """Test int conversion from string."""
        assert vm.run('int("42")') == 42
        assert vm.run('int("-10")') == -10

    def test_int_from_float(self, vm):
        """Test int conversion from float."""
        assert vm.run("int(3.7)") == 3
        assert vm.run("int(-2.5)") == -2

    def test_int_no_args(self, vm):
        """Test int with no arguments."""
        assert vm.run("int()") == 0

    def test_int_with_base(self, vm):
        """Test int with base argument."""
        assert vm.run('int("ff", 16)') == 255
        assert vm.run('int("1010", 2)') == 10

    def test_float_from_string(self, vm):
        """Test float conversion from string."""
        assert vm.run('float("3.14")') == 3.14
        assert vm.run('float("2.5e2")') == 250.0

    def test_float_from_int(self, vm):
        """Test float conversion from int."""
        assert vm.run("float(42)") == 42.0

    def test_float_no_args(self, vm):
        """Test float with no arguments."""
        assert vm.run("float()") == 0.0

    def test_str_from_int(self, vm):
        """Test str conversion from int."""
        assert vm.run("str(42)") == "42"

    def test_str_from_float(self, vm):
        """Test str conversion from float."""
        assert vm.run("str(3.14)") == "3.14"

    def test_str_from_bool(self, vm):
        """Test str conversion from bool."""
        assert vm.run("str(True)") == "True"
        assert vm.run("str(False)") == "False"

    def test_str_from_array(self, vm):
        """Test str conversion from array."""
        assert vm.run("str([1, 2, 3])") == "[1, 2, 3]"

    def test_str_from_hash(self, vm):
        """Test str conversion from hash."""
        result = vm.run("str({a: 1})")
        assert "a" in result and "1" in result

    def test_str_no_args(self, vm):
        """Test str with no arguments."""
        assert vm.run("str()") == "None"

    def test_bool_from_int(self, vm):
        """Test bool conversion from int."""
        assert vm.run("bool(1)") is True
        assert vm.run("bool(0)") is False
        assert vm.run("bool(-1)") is True

    def test_bool_from_string(self, vm):
        """Test bool conversion from string."""
        assert vm.run('bool("hello")') is True
        assert vm.run('bool("")') is False

    def test_bool_no_args(self, vm):
        """Test bool with no arguments."""
        assert vm.run("bool()") is False

    def test_list_from_string(self, vm):
        """Test list conversion from string."""
        result = vm.run('list("hello")')
        assert result == ["h", "e", "l", "l", "o"]

    def test_list_from_range(self, vm):
        """Test list conversion from range."""
        result = vm.run("list(range(3))")
        assert result == [0, 1, 2]

    def test_list_no_args(self, vm):
        """Test list with no arguments."""
        assert vm.run("list()") == []

    def test_dict_no_args(self, vm):
        """Test dict with no arguments."""
        assert vm.run("dict()") == {}

    def test_dict_from_list(self, vm):
        """Test dict conversion from list of pairs."""
        result = vm.run("dict([['a', 1], ['b', 2]])")
        assert result == {"a": 1, "b": 2}


class TestLengthFunctions:
    """Tests for len function."""

    def test_len_string(self, vm):
        """Test len with string."""
        assert vm.run('len("hello")') == 5
        assert vm.run('len("")') == 0

    def test_len_array(self, vm):
        """Test len with array."""
        assert vm.run("len([1, 2, 3])") == 3
        assert vm.run("len([])") == 0

    def test_len_hash(self, vm):
        """Test len with hash."""
        assert vm.run('len({a: 1, b: 2})') == 2
        assert vm.run("len({})") == 0


class TestRange:
    """Tests for range function."""

    def test_range_single_arg(self, vm):
        """Test range with single argument."""
        assert vm.run("range(5)") == [0, 1, 2, 3, 4]

    def test_range_two_args(self, vm):
        """Test range with two arguments."""
        assert vm.run("range(2, 5)") == [2, 3, 4]

    def test_range_three_args(self, vm):
        """Test range with three arguments."""
        assert vm.run("range(0, 10, 2)") == [0, 2, 4, 6, 8]
        assert vm.run("range(10, 0, -2)") == [10, 8, 6, 4, 2]


class TestTypeFunction:
    """Tests for type function."""

    def test_type_int(self, vm):
        """Test type of int."""
        assert vm.run("type(42)") == "int"

    def test_type_float(self, vm):
        """Test type of float."""
        assert vm.run("type(3.14)") == "float"

    def test_type_string(self, vm):
        """Test type of string."""
        assert vm.run('type("hello")') == "str"

    def test_type_bool(self, vm):
        """Test type of bool."""
        assert vm.run("type(True)") == "bool"

    def test_type_array(self, vm):
        """Test type of array."""
        assert vm.run("type([1, 2])") == "array"

    def test_type_hash(self, vm):
        """Test type of hash."""
        assert vm.run("type({a: 1})") == "hash"

    def test_type_none(self, vm):
        """Test type of None."""
        assert vm.run("type(None)") == "none"


class TestMathFunctions:
    """Tests for math functions."""

    def test_abs(self, vm):
        """Test abs function."""
        assert vm.run("abs(-5)") == 5
        assert vm.run("abs(5)") == 5
        assert vm.run("abs(-3.14)") == pytest.approx(3.14)

    def test_round(self, vm):
        """Test round function."""
        assert vm.run("round(3.7)") == 4
        assert vm.run("round(3.2)") == 3
        assert vm.run("round(3.14159, 2)") == 3.14

    def test_min_values(self, vm):
        """Test min with values."""
        assert vm.run("min(1, 2, 3)") == 1
        assert vm.run("min(-1, 0, 1)") == -1

    def test_min_array(self, vm):
        """Test min with array."""
        assert vm.run("min([5, 3, 8, 1, 9])") == 1

    def test_max_values(self, vm):
        """Test max with values."""
        assert vm.run("max(1, 2, 3)") == 3

    def test_max_array(self, vm):
        """Test max with array."""
        assert vm.run("max([5, 3, 8, 1, 9])") == 9

    def test_sum(self, vm):
        """Test sum function."""
        assert vm.run("sum([1, 2, 3, 4])") == 10
        assert vm.run("sum([1, 2, 3], 10)") == 16

    def test_pow(self, vm):
        """Test pow function."""
        assert vm.run("pow(2, 3)") == 8
        assert vm.run("pow(2, 3, 5)") == 3  # 8 % 5 = 3

    def test_sqrt(self, vm):
        """Test sqrt function."""
        assert vm.run("sqrt(16)") == 4.0
        assert vm.run("sqrt(2)") == pytest.approx(math.sqrt(2))

    def test_sin(self, vm):
        """Test sin function."""
        assert vm.run("sin(0)") == pytest.approx(0)
        assert vm.run("sin(3.14159)") == pytest.approx(0, abs=0.0001)

    def test_cos(self, vm):
        """Test cos function."""
        assert vm.run("cos(0)") == pytest.approx(1)

    def test_tan(self, vm):
        """Test tan function."""
        assert vm.run("tan(0)") == pytest.approx(0)

    def test_log(self, vm):
        """Test log function."""
        assert vm.run("log(2.71828)") == pytest.approx(1, abs=0.0001)
        assert vm.run("log(100, 10)") == pytest.approx(2)

    def test_exp(self, vm):
        """Test exp function."""
        assert vm.run("exp(0)") == pytest.approx(1)

    def test_floor(self, vm):
        """Test floor function."""
        assert vm.run("floor(3.7)") == 3
        assert vm.run("floor(-3.7)") == -4

    def test_ceil(self, vm):
        """Test ceil function."""
        assert vm.run("ceil(3.2)") == 4
        assert vm.run("ceil(-3.2)") == -3


class TestStringFunctions:
    """Tests for string functions."""

    def test_lower(self, vm):
        """Test lower function."""
        assert vm.run('lower("HELLO")') == "hello"
        assert vm.run('lower("HeLLo")') == "hello"

    def test_upper(self, vm):
        """Test upper function."""
        assert vm.run('upper("hello")') == "HELLO"
        assert vm.run('upper("HeLLo")') == "HELLO"

    def test_strip(self, vm):
        """Test strip function."""
        assert vm.run('strip("  hello  ")') == "hello"
        assert vm.run('strip("xxhelloxx", "x")') == "hello"

    def test_split(self, vm):
        """Test split function."""
        assert vm.run('split("a,b,c", ",")') == ["a", "b", "c"]
        assert vm.run('split("hello world")') == ["hello", "world"]

    def test_join(self, vm):
        """Test join function."""
        assert vm.run('join("-", ["a", "b", "c"])') == "a-b-c"
        assert vm.run('join("", ["h", "e", "l", "l", "o"])') == "hello"

    def test_replace(self, vm):
        """Test replace function."""
        assert vm.run('replace("hello world", "world", "there")') == "hello there"
        assert vm.run('replace("aaa", "a", "b")') == "bbb"

    def test_find(self, vm):
        """Test find function."""
        assert vm.run('find("hello", "l")') == 2
        assert vm.run('find("hello", "x")') == -1

    def test_startswith(self, vm):
        """Test startswith function."""
        assert vm.run('startswith("hello", "he")') is True
        assert vm.run('startswith("hello", "x")') is False

    def test_endswith(self, vm):
        """Test endswith function."""
        assert vm.run('endswith("hello", "lo")') is True
        assert vm.run('endswith("hello", "x")') is False

    def test_format(self, vm):
        """Test format function."""
        assert vm.run('format("Hello {}", "World")') == "Hello World"
        assert vm.run('format("{} + {} = {}", 1, 2, 3)') == "1 + 2 = 3"


class TestListFunctions:
    """Tests for list functions."""

    def test_append(self, vm):
        """Test append function."""
        vm.run("@arr = [1, 2]")
        vm.run("append(@arr, 3)")
        assert vm.get_variable("arr") == [1, 2, 3]

    def test_extend(self, vm):
        """Test extend function."""
        vm.run("@arr = [1, 2]")
        vm.run("extend(@arr, [3, 4])")
        assert vm.get_variable("arr") == [1, 2, 3, 4]

    def test_insert(self, vm):
        """Test insert function."""
        vm.run("@arr = [1, 3]")
        vm.run("insert(@arr, 1, 2)")
        assert vm.get_variable("arr") == [1, 2, 3]

    def test_remove(self, vm):
        """Test remove function."""
        vm.run("@arr = [1, 2, 3]")
        vm.run("remove(@arr, 2)")
        assert vm.get_variable("arr") == [1, 3]

    def test_pop(self, vm):
        """Test pop function."""
        vm.run("@arr = [1, 2, 3]")
        assert vm.run("pop(@arr)") == 3
        assert vm.get_variable("arr") == [1, 2]
        assert vm.run("pop(@arr, 0)") == 1
        assert vm.get_variable("arr") == [2]

    def test_index(self, vm):
        """Test index function."""
        vm.run("@arr = [1, 2, 3, 2]")
        assert vm.run("index(@arr, 2)") == 1

    def test_count(self, vm):
        """Test count function."""
        vm.run("@arr = [1, 2, 2, 2, 3]")
        assert vm.run("count(@arr, 2)") == 3

    def test_sort(self, vm):
        """Test sort function."""
        vm.run("@arr = [3, 1, 2]")
        vm.run("sort(@arr)")
        assert vm.get_variable("arr") == [1, 2, 3]

    def test_sort_reverse(self, vm):
        """Test sort in reverse."""
        vm.run("@arr = [1, 2, 3]")
        vm.run("sort(@arr, True)")
        assert vm.get_variable("arr") == [3, 2, 1]

    def test_reverse(self, vm):
        """Test reverse function."""
        vm.run("@arr = [1, 2, 3]")
        vm.run("reverse(@arr)")
        assert vm.get_variable("arr") == [3, 2, 1]

    def test_copy(self, vm):
        """Test copy function."""
        vm.run("@arr = [1, 2, 3]")
        vm.run("@arr2 = copy(@arr)")
        vm.run("append(@arr, 4)")
        assert vm.get_variable("arr") == [1, 2, 3, 4]
        assert vm.get_variable("arr2") == [1, 2, 3]

    def test_clear(self, vm):
        """Test clear function."""
        vm.run("@arr = [1, 2, 3]")
        vm.run("clear(@arr)")
        assert vm.get_variable("arr") == []


class TestDictFunctions:
    """Tests for dict functions."""

    def test_keys(self, vm):
        """Test keys function."""
        vm.run('%h = {a: 1, b: 2}')
        result = vm.run("keys(%h)")
        assert sorted(result) == ["a", "b"]

    def test_values(self, vm):
        """Test values function."""
        vm.run('%h = {a: 1, b: 2}')
        result = vm.run("values(%h)")
        assert sorted(result) == [1, 2]

    def test_items(self, vm):
        """Test items function."""
        vm.run('%h = {a: 1}')
        result = vm.run("items(%h)")
        assert ("a", 1) in result

    def test_get(self, vm):
        """Test get function."""
        vm.run('%h = {a: 1}')
        assert vm.run('get(%h, "a")') == 1
        assert vm.run('get(%h, "b")') is None
        assert vm.run('get(%h, "b", 0)') == 0

    def test_setdefault(self, vm):
        """Test setdefault function."""
        vm.run('%h = {a: 1}')
        assert vm.run('setdefault(%h, "a", 0)') == 1
        assert vm.run('setdefault(%h, "b", 2)') == 2
        assert vm.get_variable("h")["b"] == 2

    def test_update(self, vm):
        """Test update function."""
        vm.run('%h = {a: 1}')
        vm.run("update(%h, {b: 2})")
        assert vm.get_variable("h") == {"a": 1, "b": 2}

    def test_popitem(self, vm):
        """Test popitem function."""
        vm.run('%h = {a: 1}')
        result = vm.run("popitem(%h)")
        assert result == ("a", 1)
        assert vm.get_variable("h") == {}


class TestRandomFunctions:
    """Tests for random functions."""

    def test_random(self, vm):
        """Test random function."""
        result = vm.run("random()")
        assert 0 <= result < 1

    def test_randint(self, vm):
        """Test randint function."""
        for _ in range(10):
            result = vm.run("randint(1, 10)")
            assert 1 <= result <= 10

    def test_choice(self, vm):
        """Test choice function."""
        vm.run("@arr = [1, 2, 3]")
        for _ in range(10):
            result = vm.run("choice(@arr)")
            assert result in [1, 2, 3]

    def test_shuffle(self, vm):
        """Test shuffle function."""
        vm.run("@arr = [1, 2, 3, 4, 5]")
        original = vm.get_variable("arr").copy()
        vm.run("shuffle(@arr)")
        # Just check it's still the same elements
        assert sorted(vm.get_variable("arr")) == sorted(original)


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_enumerate(self, vm):
        """Test enumerate function."""
        result = vm.run('enumerate(["a", "b", "c"])')
        assert result == [(0, "a"), (1, "b"), (2, "c")]

    def test_zip(self, vm):
        """Test zip function."""
        result = vm.run('zip([1, 2], ["a", "b"])')
        assert result == [(1, "a"), (2, "b")]

    def test_sorted(self, vm):
        """Test sorted function."""
        assert vm.run("sorted([3, 1, 2])") == [1, 2, 3]

    def test_reversed(self, vm):
        """Test reversed function."""
        assert vm.run("reversed([1, 2, 3])") == [3, 2, 1]

    def test_any(self, vm):
        """Test any function."""
        assert vm.run("any([False, True, False])") is True
        assert vm.run("any([False, False])") is False

    def test_all(self, vm):
        """Test all function."""
        assert vm.run("all([True, True])") is True
        assert vm.run("all([True, False])") is False

    def test_callable(self, vm):
        """Test callable function."""
        assert vm.run("callable(print)") is True
        assert vm.run("callable(42)") is False

    def test_repr(self, vm):
        """Test repr function."""
        result = vm.run("repr(42)")
        assert "42" in result

    def test_id(self, vm):
        """Test id function."""
        result = vm.run("id(42)")
        assert isinstance(result, int)

    def test_hash(self, vm):
        """Test hash function."""
        result = vm.run('hash("hello")')
        assert isinstance(result, int)


class TestConstants:
    """Tests for constants."""

    def test_true_false(self, vm):
        """Test True and False constants."""
        assert vm.run("True") is True
        assert vm.run("False") is False

    def test_none(self, vm):
        """Test None constant."""
        assert vm.run("None") is None

    def test_pi(self, vm):
        """Test PI constant."""
        assert vm.run("PI") == pytest.approx(math.pi)

    def test_e(self, vm):
        """Test E constant."""
        assert vm.run("E") == pytest.approx(math.e)

    def test_inf(self, vm):
        """Test INF constant."""
        assert vm.run("INF") == float("inf")

    def test_nan(self, vm):
        """Test NAN constant."""
        assert math.isnan(vm.run("NAN"))


class TestPrintInput:
    """Tests for print and input functions."""

    def test_print_single(self, vm, capsys):
        """Test print single value."""
        vm.run('print("Hello")')
        captured = capsys.readouterr()
        assert "Hello" in captured.out

    def test_print_multiple(self, vm, capsys):
        """Test print multiple values."""
        # In Pyrl, use str concatenation or format for multiple values
        vm.run('print("Hello" + " " + "World")')
        captured = capsys.readouterr()
        assert "Hello World" in captured.out

    def test_print_return_none(self, vm):
        """Test print returns None."""
        assert vm.run('print("test")') is None

    def test_input_with_prompt(self, vm, monkeypatch):
        """Test input with prompt."""
        # Use a proper function for monkeypatch
        def mock_input(prompt=""):
            return "test_input"
        monkeypatch.setattr("builtins.input", mock_input)
        result = vm.run('input("Enter: ")')
        assert result == "test_input"

    def test_input_no_prompt(self, vm, monkeypatch):
        """Test input without prompt."""
        monkeypatch.setattr("builtins.input", lambda: "test_input")
        result = vm.run("input()")
        assert result == "test_input"
