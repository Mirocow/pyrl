# FILE: tests/test_builtins.py
"""
Comprehensive tests for built-in functions
Tests: all built-in functions in PyrlVM
"""

import pytest
from pyrl_vm import PyrlVM, PyrlTypeError


class TestBuiltinFunctions:
    """Test all built-in functions"""
    
    @pytest.fixture
    def vm(self):
        """Create a fresh VM"""
        return PyrlVM()


class TestStringFunctions(TestBuiltinFunctions):
    """Test string manipulation functions"""
    
    def test_upper(self, vm):
        """Test upper function"""
        vm.execute('$result = &upper("hello")')
        assert vm.get_variable('$result') == 'HELLO'
    
    def test_lower(self, vm):
        """Test lower function"""
        vm.execute('$result = &lower("HELLO")')
        assert vm.get_variable('$result') == 'hello'
    
    def test_trim(self, vm):
        """Test trim function"""
        vm.execute('$result = &trim("  hello  ")')
        assert vm.get_variable('$result') == 'hello'
    
    def test_str(self, vm):
        """Test str function"""
        vm.execute('$result = &str(42)')
        assert vm.get_variable('$result') == '42'
        assert isinstance(vm.get_variable('$result'), str)
    
    def test_split_no_delimiter(self, vm):
        """Test split without delimiter"""
        vm.execute('$result = &split("a b c")')
        assert vm.get_variable('$result') == ['a', 'b', 'c']
    
    def test_split_with_delimiter(self, vm):
        """Test split with delimiter"""
        vm.execute('$result = &split("a,b,c", ",")')
        assert vm.get_variable('$result') == ['a', 'b', 'c']
    
    def test_join_default(self, vm):
        """Test join with default delimiter"""
        vm.execute('@arr = ["a", "b", "c"]')
        vm.execute('$result = &join(@arr)')
        assert vm.get_variable('$result') == 'abc'
    
    def test_join_with_delimiter(self, vm):
        """Test join with delimiter"""
        vm.execute('@arr = ["a", "b", "c"]')
        vm.execute('$result = &join(@arr, "-")')
        assert vm.get_variable('$result') == 'a-b-c'


class TestTypeFunctions(TestBuiltinFunctions):
    """Test type conversion and checking functions"""
    
    def test_type_string(self, vm):
        """Test type function with string"""
        vm.execute('$result = &type("hello")')
        assert vm.get_variable('$result') == 'str'
    
    def test_type_int(self, vm):
        """Test type function with int"""
        vm.execute('$result = &type(42)')
        assert vm.get_variable('$result') == 'int'
    
    def test_type_list(self, vm):
        """Test type function with list"""
        vm.execute('@arr = [1, 2, 3]')
        vm.execute('$result = &type(@arr)')
        assert vm.get_variable('$result') == 'list'
    
    def test_type_dict(self, vm):
        """Test type function with dict"""
        vm.execute('%h = {"a": 1}')
        vm.execute('$result = &type(%h)')
        assert vm.get_variable('$result') == 'dict'
    
    def test_int_from_string(self, vm):
        """Test int conversion from string"""
        vm.execute('$result = &int("42")')
        assert vm.get_variable('$result') == 42
        assert isinstance(vm.get_variable('$result'), int)
    
    def test_int_from_float(self, vm):
        """Test int from value"""
        vm.execute('$result = &int("3.9")')
        # int("3.9") would fail, but our int function handles it
        assert vm.get_variable('$result') == 3
    
    def test_float_from_string(self, vm):
        """Test float conversion from string"""
        vm.execute('$result = &float("3.14")')
        assert vm.get_variable('$result') == 3.14
        assert isinstance(vm.get_variable('$result'), float)


class TestArrayFunctions(TestBuiltinFunctions):
    """Test array manipulation functions"""
    
    def test_len_string(self, vm):
        """Test len with string"""
        vm.execute('$result = &len("hello")')
        assert vm.get_variable('$result') == 5
    
    def test_len_array(self, vm):
        """Test len with array"""
        vm.execute('@arr = [1, 2, 3, 4, 5]')
        vm.execute('$result = &len(@arr)')
        assert vm.get_variable('$result') == 5
    
    def test_len_empty(self, vm):
        """Test len with empty array"""
        vm.execute('@arr = []')
        vm.execute('$result = &len(@arr)')
        assert vm.get_variable('$result') == 0
    
    def test_push(self, vm):
        """Test push function"""
        vm.execute('@arr = [1, 2]')
        vm.execute('&push(@arr, 3)')
        assert vm.get_variable('@arr') == [1, 2, 3]
    
    def test_pop(self, vm):
        """Test pop function"""
        vm.execute('@arr = [1, 2, 3]')
        vm.execute('$last = &pop(@arr)')
        assert vm.get_variable('$last') == 3
        assert vm.get_variable('@arr') == [1, 2]
    
    def test_pop_empty(self, vm):
        """Test pop on empty array"""
        vm.execute('@arr = []')
        vm.execute('$result = &pop(@arr)')
        assert vm.get_variable('$result') is None
    
    def test_push_type_error(self, vm):
        """Test push with non-array raises error"""
        vm.execute('$not_array = 5')
        with pytest.raises(PyrlTypeError):
            vm.execute('&push($not_array, 1)')
    
    def test_pop_type_error(self, vm):
        """Test pop with non-array raises error"""
        vm.execute('$not_array = 5')
        with pytest.raises(PyrlTypeError):
            vm.execute('&pop($not_array)')
    
    def test_range(self, vm):
        """Test range function"""
        vm.execute('@r = &range(5)')
        assert vm.get_variable('@r') == [0, 1, 2, 3, 4]
    
    def test_min(self, vm):
        """Test min function"""
        vm.execute('@nums = [5, 2, 8, 1, 9]')
        vm.execute('$result = &min(@nums)')
        assert vm.get_variable('$result') == 1
    
    def test_max(self, vm):
        """Test max function"""
        vm.execute('@nums = [5, 2, 8, 1, 9]')
        vm.execute('$result = &max(@nums)')
        assert vm.get_variable('$result') == 9
    
    def test_sum(self, vm):
        """Test sum function"""
        vm.execute('@nums = [1, 2, 3, 4, 5]')
        vm.execute('$result = &sum(@nums)')
        assert vm.get_variable('$result') == 15
    
    def test_sorted(self, vm):
        """Test sorted function"""
        vm.execute('@nums = [3, 1, 4, 1, 5, 9, 2, 6]')
        vm.execute('@sorted = &sorted(@nums)')
        assert vm.get_variable('@sorted') == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_reversed(self, vm):
        """Test reversed function"""
        vm.execute('@nums = [1, 2, 3]')
        vm.execute('@rev = &reversed(@nums)')
        assert vm.get_variable('@rev') == [3, 2, 1]
    
    def test_min_empty(self, vm):
        """Test min on empty array"""
        vm.execute('@empty = []')
        vm.execute('$result = &min(@empty)')
        assert vm.get_variable('$result') is None
    
    def test_max_empty(self, vm):
        """Test max on empty array"""
        vm.execute('@empty = []')
        vm.execute('$result = &max(@empty)')
        assert vm.get_variable('$result') is None
    
    def test_sum_empty(self, vm):
        """Test sum on empty array"""
        vm.execute('@empty = []')
        vm.execute('$result = &sum(@empty)')
        assert vm.get_variable('$result') == 0


class TestHashFunctions(TestBuiltinFunctions):
    """Test hash manipulation functions"""
    
    def test_keys(self, vm):
        """Test keys function"""
        vm.execute('%h = {"a": 1, "b": 2, "c": 3}')
        vm.execute('@keys = &keys(%h)')
        keys = vm.get_variable('@keys')
        assert set(keys) == {'a', 'b', 'c'}
    
    def test_values(self, vm):
        """Test values function"""
        vm.execute('%h = {"a": 1, "b": 2, "c": 3}')
        vm.execute('@values = &values(%h)')
        values = vm.get_variable('@values')
        assert set(values) == {1, 2, 3}
    
    def test_keys_empty(self, vm):
        """Test keys on empty hash"""
        vm.execute('%h = {}')
        vm.execute('@keys = &keys(%h)')
        assert vm.get_variable('@keys') == []
    
    def test_values_empty(self, vm):
        """Test values on empty hash"""
        vm.execute('%h = {}')
        vm.execute('@values = &values(%h)')
        assert vm.get_variable('@values') == []
    
    def test_keys_non_dict(self, vm):
        """Test keys on non-dict returns empty"""
        vm.execute('$not_dict = 5')
        vm.execute('@keys = &keys($not_dict)')
        assert vm.get_variable('@keys') == []


class TestMathFunctions(TestBuiltinFunctions):
    """Test math functions"""
    
    def test_abs_positive(self, vm):
        """Test abs with positive"""
        vm.execute('$result = &abs(42)')
        assert vm.get_variable('$result') == 42
    
    def test_abs_negative(self, vm):
        """Test abs with negative"""
        vm.execute('$result = &abs(-42)')
        assert vm.get_variable('$result') == 42
    
    def test_round_default(self, vm):
        """Test round with default precision"""
        vm.execute('$result = &round(3.7)')
        assert vm.get_variable('$result') == 4
    
    def test_round_precision(self, vm):
        """Test round with precision"""
        vm.execute('$result = &round(3.14159, 2)')
        assert vm.get_variable('$result') == 3.14


class TestFunctionChaining(TestBuiltinFunctions):
    """Test chaining multiple functions"""
    
    def test_chain_upper_lower(self, vm):
        """Test chaining upper then lower"""
        vm.execute('$result = &lower(&upper("hello"))')
        assert vm.get_variable('$result') == 'hello'
    
    def test_chain_str_len(self, vm):
        """Test chaining str and len"""
        vm.execute('$result = &len(&str(12345))')
        assert vm.get_variable('$result') == 5
    
    def test_chain_split_join(self, vm):
        """Test chaining split and join"""
        vm.execute('$result = &join(&split("a,b,c", ","), "-")')
        assert vm.get_variable('$result') == 'a-b-c'
    
    def test_chain_sorted_reversed(self, vm):
        """Test chaining sorted and reversed"""
        vm.execute('@nums = [3, 1, 4, 1, 5]')
        vm.execute('@result = &reversed(&sorted(@nums))')
        assert vm.get_variable('@result') == [5, 4, 3, 1, 1]


class TestBuiltinEdgeCases(TestBuiltinFunctions):
    """Test edge cases for built-in functions"""
    
    def test_int_empty(self, vm):
        """Test int with empty/none"""
        vm.execute('$result = &int(none)')
        assert vm.get_variable('$result') == 0
    
    def test_float_empty(self, vm):
        """Test float with empty/none"""
        vm.execute('$result = &float(none)')
        assert vm.get_variable('$result') == 0.0
    
    def test_len_none(self, vm):
        """Test len with none"""
        vm.execute('$result = &len(none)')
        assert vm.get_variable('$result') == 1
    
    def test_upper_number(self, vm):
        """Test upper with number"""
        vm.execute('$result = &upper(123)')
        assert vm.get_variable('$result') == '123'
    
    def test_lower_number(self, vm):
        """Test lower with number"""
        vm.execute('$result = &lower(123)')
        assert vm.get_variable('$result') == '123'


class TestFunctionRegistration(TestBuiltinFunctions):
    """Test function registration"""
    
    def test_register_custom_function(self, vm):
        """Test registering custom function"""
        vm.register_function('&custom', lambda x: x * 2)
        vm.execute('$result = &custom(5)')
        assert vm.get_variable('$result') == 10
    
    def test_register_without_sigil(self, vm):
        """Test registering without sigil raises error"""
        with pytest.raises(ValueError):
            vm.register_function('custom', lambda x: x)
    
    def test_override_builtin(self, vm):
        """Test overriding built-in function"""
        vm.register_function('&len', lambda x: 999)
        vm.execute('$result = &len("hello")')
        assert vm.get_variable('$result') == 999
