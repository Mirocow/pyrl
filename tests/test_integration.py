# FILE: tests/test_integration.py
"""
Integration tests for Pyrl VM
Tests: full code execution scenarios
"""

import pytest
from pyrl_vm import PyrlVM, PyrlSyntaxError, PyrlRuntimeError


class TestIntegration:
    """Integration tests for complete code execution"""
    
    @pytest.fixture
    def vm(self):
        """Create a fresh VM"""
        return PyrlVM()


class TestUserAuthSystem(TestIntegration):
    """Test building a user authentication system"""
    
    def test_user_management(self, vm):
        """Test user management system"""
        code = '''
            %users = {
                "admin": {
                    "password": "admin123",
                    "role": "administrator"
                },
                "user": {
                    "password": "user123",
                    "role": "member"
                }
            }
            
            &check_login($username, $password) = {
                $user = %users[$username]
                if $user == none {
                    return "User not found"
                }
                if $user["password"] == $password {
                    return "Login successful"
                }
                return "Invalid password"
            }
            
            $result = &check_login("admin", "admin123")
        '''
        vm.execute(code)
        # Result stored in memory
        assert 'users' in vm.memory['hashes']
    
    def test_password_validation(self, vm):
        """Test password validation with regex"""
        code = '''
            $password = "SecurePass123"
            $pattern = r"^[a-zA-Z0-9]{8,}$"
            
            $valid = $password =~ $pattern
        '''
        vm.execute(code)
        assert vm.get_variable('$valid') == True


class TestShoppingCart(TestIntegration):
    """Test shopping cart functionality"""
    
    def test_cart_operations(self, vm):
        """Test cart add and total"""
        code = '''
            @cart = []
            $total = 0
            
            &add_item($name, $price, $qty) = {
                &push(@cart, {"name": $name, "price": $price, "qty": $qty})
            }
            
            &calculate_total() = {
                $sum = 0
                for $item in @cart {
                    $sum = $sum + $item["price"] * $item["qty"]
                }
                return $sum
            }
            
            &add_item("Laptop", 999, 1)
            &add_item("Mouse", 29, 2)
            
            $total = &calculate_total()
        '''
        vm.execute(code)
        # Cart should have items
        cart = vm.get_variable('@cart')
        assert len(cart) == 2


class TestTodoList(TestIntegration):
    """Test todo list functionality"""
    
    def test_todo_operations(self, vm):
        """Test todo add, complete, list"""
        code = '''
            @todos = []
            
            &add_todo($task) = {
                &push(@todos, {"task": $task, "done": false})
            }
            
            &complete_todo($index) = {
                $todo = @todos[$index]
                $todo["done"] = true
                @todos[$index] = $todo
            }
            
            &add_todo("Write tests")
            &add_todo("Run tests")
            &complete_todo(0)
        '''
        vm.execute(code)
        todos = vm.get_variable('@todos')
        assert len(todos) == 2
        assert todos[0]['done'] == True


class TestCalculator(TestIntegration):
    """Test calculator functionality"""
    
    def test_basic_operations(self, vm):
        """Test basic calculator"""
        code = '''
            &add($a, $b) = { return $a + $b }
            &sub($a, $b) = { return $a - $b }
            &mul($a, $b) = { return $a * $b }
            &div($a, $b) = { return $a / $b }
            
            $sum = &add(10, 5)
            $diff = &sub(10, 5)
            $product = &mul(10, 5)
            $quotient = &div(10, 5)
        '''
        vm.execute(code)
        assert vm.get_variable('$sum') == 15
        assert vm.get_variable('$diff') == 5
        assert vm.get_variable('$product') == 50
        assert vm.get_variable('$quotient') == 2.0
    
    def test_scientific_calculator(self, vm):
        """Test scientific calculator functions"""
        code = '''
            &square($x) = { return $x * $x }
            &cube($x) = { return $x * $x * $x }
            &power($base, $exp) = {
                $result = 1
                for $i in &range($exp) {
                    $result = $result * $base
                }
                return $result
            }
            
            $sq = &square(5)
            $cb = &cube(3)
            $pow = &power(2, 10)
        '''
        vm.execute(code)
        assert vm.get_variable('$sq') == 25
        assert vm.get_variable('$cb') == 27
        assert vm.get_variable('$pow') == 1024


class TestStringProcessing(TestIntegration):
    """Test string processing functionality"""
    
    def test_text_analysis(self, vm):
        """Test text analysis"""
        code = '''
            $text = "Hello World Hello Pyrl"
            
            @words = &split($text, " ")
            $word_count = &len(@words)
            
            $upper_text = &upper($text)
            $lower_text = &lower($text)
        '''
        vm.execute(code)
        assert vm.get_variable('$word_count') == 4
        assert 'HELLO' in vm.get_variable('$upper_text')
    
    def test_string_validation(self, vm):
        """Test string validation"""
        code = '''
            $email = "test@example.com"
            $email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
            
            $valid_email = $email =~ $email_pattern
            
            $phone = "123-456-7890"
            $phone_pattern = r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$"
            
            $valid_phone = $phone =~ $phone_pattern
        '''
        vm.execute(code)
        assert vm.get_variable('$valid_email') == True
        assert vm.get_variable('$valid_phone') == True


class TestDataStructures(TestIntegration):
    """Test data structure implementations"""
    
    def test_stack_implementation(self, vm):
        """Test stack using array"""
        code = '''
            @stack = []
            
            &push_stack($item) = {
                &push(@stack, $item)
            }
            
            &pop_stack() = {
                return &pop(@stack)
            }
            
            &peek_stack() = {
                $len = &len(@stack)
                if $len == 0 {
                    return none
                }
                return @stack[$len - 1]
            }
            
            &push_stack(1)
            &push_stack(2)
            &push_stack(3)
            
            $top = &peek_stack()
            $popped = &pop_stack()
        '''
        vm.execute(code)
        assert vm.get_variable('$top') == 3
        assert vm.get_variable('$popped') == 3
    
    def test_queue_implementation(self, vm):
        """Test simple queue"""
        code = '''
            @queue = []
            
            &enqueue($item) = {
                &push(@queue, $item)
            }
            
            &dequeue() = {
                $first = @queue[0]
                @queue = &reversed(@queue)
                &pop(@queue)
                @queue = &reversed(@queue)
                return $first
            }
            
            &enqueue("first")
            &enqueue("second")
            &enqueue("third")
            
            $item = &dequeue()
        '''
        vm.execute(code)
        assert vm.get_variable('$item') == 'first'


class TestAlgorithms(TestIntegration):
    """Test algorithm implementations"""
    
    def test_factorial(self, vm):
        """Test factorial algorithm"""
        code = '''
            &factorial($n) = {
                if $n <= 1 {
                    return 1
                }
                return $n * &factorial($n - 1)
            }
            
            $fact5 = &factorial(5)
            $fact10 = &factorial(10)
        '''
        vm.execute(code)
        assert vm.get_variable('$fact5') == 120
        assert vm.get_variable('$fact10') == 3628800
    
    def test_fibonacci(self, vm):
        """Test Fibonacci sequence"""
        code = '''
            &fib($n) = {
                if $n <= 0 {
                    return 0
                }
                if $n == 1 {
                    return 1
                }
                return &fib($n - 1) + &fib($n - 2)
            }
            
            @fib_sequence = []
            for $i in &range(10) {
                &push(@fib_sequence, &fib($i))
            }
        '''
        vm.execute(code)
        seq = vm.get_variable('@fib_sequence')
        assert seq == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    def test_sum_algorithm(self, vm):
        """Test sum algorithm"""
        code = '''
            @numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            
            $total = 0
            for $n in @numbers {
                $total = $total + $n
            }
        '''
        vm.execute(code)
        assert vm.get_variable('$total') == 55


class TestVueComponentGeneration(TestIntegration):
    """Test Vue component generation integration"""
    
    def test_user_card_component(self, vm):
        """Test generating user card Vue component"""
        code = '''
            %user = {
                "name": "Alice",
                "email": "alice@example.com",
                "role": "Admin"
            }
            
            $vue_code = vue "UserCard" {
                name: %user["name"],
                email: %user["email"],
                role: %user["role"]
            }
        '''
        result = vm.execute(code)
        assert '<template>' in result
        assert 'Alice' in result
    
    def test_list_component(self, vm):
        """Test generating list Vue component"""
        code = '''
            @items = ["Apple", "Banana", "Cherry"]
            
            $vue_code = vue "FruitList" {
                items: @items
            }
        '''
        result = vm.execute(code)
        assert 'v-for' in result
        assert 'FruitList' in result


class TestErrorHandling(TestIntegration):
    """Test error handling scenarios"""
    
    def test_division_by_zero(self, vm):
        """Test division by zero handling"""
        with pytest.raises(PyrlRuntimeError):
            vm.execute('$x = 10 / 0')
    
    def test_invalid_function_call(self, vm):
        """Test invalid function call"""
        with pytest.raises(PyrlRuntimeError):
            vm.execute('$result = &nonexistent()')
    
    def test_syntax_error(self, vm):
        """Test syntax error handling"""
        with pytest.raises(PyrlSyntaxError):
            vm.execute('invalid code here')


class TestCompleteApplications(TestIntegration):
    """Test complete application scenarios"""
    
    def test_counter_app(self, vm):
        """Test counter application"""
        code = '''
            $count = 0
            
            &increment() = {
                $count = $count + 1
                return $count
            }
            
            &decrement() = {
                $count = $count - 1
                return $count
            }
            
            &reset() = {
                $count = 0
                return $count
            }
            
            &increment()
            &increment()
            &increment()
            &decrement()
        '''
        vm.execute(code)
        assert vm.get_variable('$count') == 2
    
    def test_temperature_converter(self, vm):
        """Test temperature converter"""
        code = '''
            &celsius_to_fahrenheit($c) = {
                return $c * 9 / 5 + 32
            }
            
            &fahrenheit_to_celsius($f) = {
                return ($f - 32) * 5 / 9
            }
            
            $f = &celsius_to_fahrenheit(0)
            $c = &fahrenheit_to_celsius(212)
        '''
        vm.execute(code)
        assert vm.get_variable('$f') == 32.0
        assert vm.get_variable('$c') == 100.0
    
    def test_grade_calculator(self, vm):
        """Test grade calculator"""
        code = '''
            &calculate_grade($score) = {
                if $score >= 90 {
                    return "A"
                }
                if $score >= 80 {
                    return "B"
                }
                if $score >= 70 {
                    return "C"
                }
                if $score >= 60 {
                    return "D"
                }
                return "F"
            }
            
            $grade_a = &calculate_grade(95)
            $grade_b = &calculate_grade(85)
            $grade_c = &calculate_grade(75)
            $grade_d = &calculate_grade(65)
            $grade_f = &calculate_grade(55)
        '''
        vm.execute(code)
        assert vm.get_variable('$grade_a') == 'A'
        assert vm.get_variable('$grade_b') == 'B'
        assert vm.get_variable('$grade_c') == 'C'
        assert vm.get_variable('$grade_d') == 'D'
        assert vm.get_variable('$grade_f') == 'F'
