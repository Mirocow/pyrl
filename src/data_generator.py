# FILE: data_generator.py
"""
Pyrl Training Data Generator
Generates training datasets for fine-tuning AI models on Pyrl language

Version: 1.0.0
Author: Pyrl Ecosystem Team

Features:
- Generates code-comment pairs
- Creates diverse examples across all language features
- Outputs JSONL format for SFT training
- Supports multiple difficulty levels
"""

import json
import random
import os
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrainingExample:
    """Single training example for SFT"""
    instruction: str
    input: str
    output: str
    category: str
    difficulty: str  # easy, medium, hard
    metadata: Dict[str, Any] = None


class PyrlDataGenerator:
    """Generates training data for Pyrl language model"""
    
    def __init__(self):
        self.examples: List[TrainingExample] = []
        self.categories = [
            "variables",
            "arrays",
            "hashes",
            "functions",
            "conditionals",
            "loops",
            "regex",
            "vue",
            "testing",
            "plugins",
            "algorithms",
            "web_app"
        ]
    
    def generate_all(self) -> List[TrainingExample]:
        """Generate all training examples"""
        self.examples = []
        
        # Generate examples for each category
        self._generate_variables()
        self._generate_arrays()
        self._generate_hashes()
        self._generate_functions()
        self._generate_conditionals()
        self._generate_loops()
        self._generate_regex()
        self._generate_vue()
        self._generate_testing()
        self._generate_plugins()
        self._generate_algorithms()
        self._generate_web_app()
        
        return self.examples
    
    def _add_example(self, instruction: str, input_code: str, output_code: str,
                     category: str, difficulty: str = "medium", metadata: Dict = None):
        """Add a training example"""
        self.examples.append(TrainingExample(
            instruction=instruction,
            input=input_code,
            output=output_code,
            category=category,
            difficulty=difficulty,
            metadata=metadata or {}
        ))
    
    # ========================================================================
    # VARIABLES
    # ========================================================================
    
    def _generate_variables(self):
        """Generate variable-related examples"""
        
        # Scalar variables
        self._add_example(
            instruction="Create scalar variables with different data types",
            input_code="Create a scalar variable for name (John), age (25), and active status (true)",
            output_code='''# Scalar variable declarations
$name = "John"
$age = 25
$active = true

# Print the values
print($name)
print($age)
print($active)''',
            category="variables",
            difficulty="easy"
        )
        
        # String operations
        self._add_example(
            instruction="Demonstrate string concatenation and operations",
            input_code="Concatenate first name and last name with a space between them",
            output_code='''# String concatenation
$first = "John"
$last = "Doe"
$full = $first + " " + $last

# String operations
$upper = &upper($full)
$lower = &lower($full)
$trimmed = &trim("  hello  ")

print($full)
print($upper)
print($lower)''',
            category="variables",
            difficulty="easy"
        )
        
        # Number operations
        self._add_example(
            instruction="Perform arithmetic operations on scalar variables",
            input_code="Calculate the sum, difference, product, and quotient of two numbers",
            output_code='''# Arithmetic operations
$a = 10
$b = 3

$sum = $a + $b
$diff = $a - $b
$product = $a * $b
$quotient = $a / $b
$modulo = $a % $b

print("Sum: " + &str($sum))
print("Difference: " + &str($diff))
print("Product: " + &str($product))
print("Quotient: " + &str($quotient))
print("Modulo: " + &str($modulo))''',
            category="variables",
            difficulty="easy"
        )
        
        # Type conversions
        self._add_example(
            instruction="Convert between different data types",
            input_code="Convert a string number to integer and perform calculations",
            output_code='''# Type conversion
$str_num = "42"
$int_num = &int($str_num)
$float_num = &float($str_num)

# Perform calculations
$result = $int_num * 2
$pi_approx = 3.14159
$rounded = &round($pi_approx, 2)

print($result)
print($rounded)''',
            category="variables",
            difficulty="medium"
        )
    
    # ========================================================================
    # ARRAYS
    # ========================================================================
    
    def _generate_arrays(self):
        """Generate array-related examples"""
        
        # Array creation
        self._add_example(
            instruction="Create and manipulate arrays",
            input_code="Create an array of fruits and demonstrate basic array operations",
            output_code='''# Array creation
@fruits = ["apple", "banana", "cherry", "date"]

# Array access
$first = @fruits[0]
$third = @fruits[2]

# Array length
$count = &len(@fruits)

# Add elements
&push(@fruits, "elderberry")

# Remove last element
$last = &pop(@fruits)

print("First fruit: " + $first)
print("Fruit count: " + &str($count))''',
            category="arrays",
            difficulty="easy"
        )
        
        # Array iteration
        self._add_example(
            instruction="Iterate over an array and process each element",
            input_code="Create a shopping list and calculate the total length of all item names",
            output_code='''# Shopping list array
@shopping = ["milk", "bread", "eggs", "cheese", "butter"]

# Process each item
$total_length = 0
for $item in @shopping {
    $len = &len($item)
    $total_length = $total_length + $len
    print("Item: " + $item + " (length: " + &str($len) + ")")
}

print("Total characters: " + &str($total_length))''',
            category="arrays",
            difficulty="medium"
        )
        
        # Array sorting and manipulation
        self._add_example(
            instruction="Sort arrays and find min/max values",
            input_code="Create an array of numbers and find the min, max, and sorted order",
            output_code='''# Number array
@numbers = [42, 17, 8, 99, 23, 56, 4]

# Find extremes
$min_val = &min(@numbers)
$max_val = &max(@numbers)
$sum = &sum(@numbers)

# Sort the array
@sorted_asc = &sorted(@numbers)
@sorted_desc = &reversed(@sorted_asc)

print("Min: " + &str($min_val))
print("Max: " + &str($max_val))
print("Sum: " + &str($sum))
print("Sorted: " + &join(@sorted_asc, ", "))''',
            category="arrays",
            difficulty="medium"
        )
    
    # ========================================================================
    # HASHES
    # ========================================================================
    
    def _generate_hashes(self):
        """Generate hash/dict-related examples"""
        
        # Hash creation
        self._add_example(
            instruction="Create and access hash (dictionary) data",
            input_code="Create a user profile hash with name, email, and age",
            output_code='''# Hash creation
%user = {
    "name": "Alice Smith",
    "email": "alice@example.com",
    "age": 28,
    "active": true
}

# Access hash values
$name = %user["name"]
$email = %user["email"]
$age = %user["age"]

# Modify hash values
%user["age"] = 29
%user["city"] = "New York"

print("User: " + $name)
print("Email: " + $email)
print("Age: " + &str(%user["age"]))''',
            category="hashes",
            difficulty="easy"
        )
        
        # Nested hashes
        self._add_example(
            instruction="Work with nested hash structures",
            input_code="Create a nested hash representing a product with details and pricing",
            output_code='''# Nested hash structure
%product = {
    "name": "Laptop",
    "details": {
        "brand": "TechCorp",
        "model": "ProBook X1",
        "specs": {
            "ram": 16,
            "storage": 512,
            "screen": 15.6
        }
    },
    "pricing": {
        "base": 999,
        "discount": 100,
        "currency": "USD"
    }
}

# Access nested values
$brand = %product["details"]["brand"]
$ram = %product["details"]["specs"]["ram"]
$final_price = %product["pricing"]["base"] - %product["pricing"]["discount"]

print("Brand: " + $brand)
print("RAM: " + &str($ram) + "GB")
print("Price: $" + &str($final_price))''',
            category="hashes",
            difficulty="medium"
        )
        
        # Hash iteration
        self._add_example(
            instruction="Iterate over hash keys and values",
            input_code="Create a configuration hash and print all settings",
            output_code='''# Configuration hash
%config = {
    "host": "localhost",
    "port": 8080,
    "debug": true,
    "timeout": 30
}

# Get keys and values
@keys = &keys(%config)
@values = &values(%config)

# Print all settings
print("Configuration Settings:")
for $key in @keys {
    $value = %config[$key]
    print("  " + $key + ": " + &str($value))
}''',
            category="hashes",
            difficulty="medium"
        )
    
    # ========================================================================
    # FUNCTIONS
    # ========================================================================
    
    def _generate_functions(self):
        """Generate function-related examples"""
        
        # Basic function
        self._add_example(
            instruction="Define and call a simple function",
            input_code="Create a function that greets a person by name",
            output_code='''# Function definition
&greet($name) = {
    $message = "Hello, " + $name + "!"
    return $message
}

# Function calls
$greeting1 = &greet("Alice")
$greeting2 = &greet("Bob")

print($greeting1)
print($greeting2)''',
            category="functions",
            difficulty="easy"
        )
        
        # Function with multiple parameters
        self._add_example(
            instruction="Create a function with multiple parameters and return value",
            input_code="Create a function to calculate the area of a rectangle",
            output_code='''# Rectangle area function
&rectangle_area($width, $height) = {
    $area = $width * $height
    return $area
}

# Rectangle perimeter function
&rectangle_perimeter($width, $height) = {
    $perimeter = 2 * ($width + $height)
    return $perimeter
}

# Calculate for a 5x3 rectangle
$w = 5
$h = 3
$area = &rectangle_area($w, $h)
$perimeter = &rectangle_perimeter($w, $h)

print("Rectangle " + &str($w) + "x" + &str($h))
print("Area: " + &str($area))
print("Perimeter: " + &str($perimeter))''',
            category="functions",
            difficulty="medium"
        )
        
        # Recursive function
        self._add_example(
            instruction="Implement a recursive function",
            input_code="Create a recursive function to calculate factorial",
            output_code='''# Factorial function (recursive)
&factorial($n) = {
    if $n <= 1 {
        return 1
    }
    return $n * &factorial($n - 1)
}

# Fibonacci function (recursive)
&fibonacci($n) = {
    if $n <= 0 {
        return 0
    }
    if $n == 1 {
        return 1
    }
    return &fibonacci($n - 1) + &fibonacci($n - 2)
}

# Test the functions
print("Factorial of 5: " + &str(&factorial(5)))
print("Fibonacci of 10: " + &str(&fibonacci(10)))''',
            category="functions",
            difficulty="hard"
        )
    
    # ========================================================================
    # CONDITIONALS
    # ========================================================================
    
    def _generate_conditionals(self):
        """Generate conditional-related examples"""
        
        # If-else
        self._add_example(
            instruction="Use conditional statements for decision making",
            input_code="Check if a number is positive, negative, or zero",
            output_code='''# Number classification
$num = -5

if $num > 0 {
    print(&str($num) + " is positive")
}
if $num < 0 {
    print(&str($num) + " is negative")
}
if $num == 0 {
    print("The number is zero")
}''',
            category="conditionals",
            difficulty="easy"
        )
        
        # If-else chain
        self._add_example(
            instruction="Create a grade calculator with conditional logic",
            input_code="Convert a numerical score to a letter grade",
            output_code='''# Grade calculator
$score = 85
$grade = ""

if $score >= 90 {
    $grade = "A"
}
if $score >= 80 {
    if $score < 90 {
        $grade = "B"
    }
}
if $score >= 70 {
    if $score < 80 {
        $grade = "C"
    }
}
if $score >= 60 {
    if $score < 70 {
        $grade = "D"
    }
}
if $score < 60 {
    $grade = "F"
}

print("Score: " + &str($score))
print("Grade: " + $grade)''',
            category="conditionals",
            difficulty="medium"
        )
        
        # Complex conditions
        self._add_example(
            instruction="Use logical operators in conditions",
            input_code="Check eligibility based on multiple criteria",
            output_code='''# Eligibility checker
$age = 25
$has_license = true
$has_experience = true
$no_violations = true

# Check driving eligibility
$is_eligible = $age >= 21 && $has_license && $has_experience
$is_clean = $no_violations || $age > 30

if $is_eligible && $is_clean {
    print("Eligible for premium insurance")
}
if $is_eligible && !$is_clean {
    print("Eligible for standard insurance")
}
if !$is_eligible {
    print("Not eligible for insurance")
}''',
            category="conditionals",
            difficulty="medium"
        )
    
    # ========================================================================
    # LOOPS
    # ========================================================================
    
    def _generate_loops(self):
        """Generate loop-related examples"""
        
        # For loop
        self._add_example(
            instruction="Use for loop to iterate over a range",
            input_code="Print numbers 1 to 10 and their squares",
            output_code='''# Print squares from 1 to 10
@range = &range(11)

for $i in @range {
    if $i > 0 {
        $square = $i * $i
        print(&str($i) + " squared = " + &str($square))
    }
}''',
            category="loops",
            difficulty="easy"
        )
        
        # While loop
        self._add_example(
            instruction="Use while loop for iterative calculation",
            input_code="Find the largest power of 2 less than 1000",
            output_code='''# Find largest power of 2 under 1000
$power = 1
$count = 0

while $power < 1000 {
    $power = $power * 2
    $count = $count + 1
}

# Back up one step (went over)
$power = $power / 2
$count = $count - 1

print("Largest power of 2 under 1000: " + &str($power))
print("Exponent: " + &str($count))''',
            category="loops",
            difficulty="medium"
        )
        
        # Nested loops
        self._add_example(
            instruction="Create nested loops for pattern generation",
            input_code="Generate a multiplication table",
            output_code='''# Multiplication table (1-5)
@nums = [1, 2, 3, 4, 5]

print("Multiplication Table:")
for $i in @nums {
    $row = ""
    for $j in @nums {
        $product = $i * $j
        $row = $row + &str($product) + " "
    }
    print($row)
}''',
            category="loops",
            difficulty="medium"
        )
    
    # ========================================================================
    # REGEX
    # ========================================================================
    
    def _generate_regex(self):
        """Generate regex-related examples"""
        
        # Basic regex matching
        self._add_example(
            instruction="Use regex to validate input patterns",
            input_code="Validate if a string is a valid email format",
            output_code='''# Email validation
$email1 = "user@example.com"
$email2 = "invalid-email"

# Email regex pattern
$email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

if $email1 =~ $email_pattern {
    print($email1 + " is a valid email")
}
if $email2 !~ $email_pattern {
    print($email2 + " is NOT a valid email")
}''',
            category="regex",
            difficulty="medium"
        )
        
        # Phone number validation
        self._add_example(
            instruction="Validate phone number format",
            input_code="Check if phone numbers match the expected format",
            output_code='''# Phone validation
@phones = ["+1-555-123-4567", "555-1234", "+44 20 7946 0958", "invalid"]

$phone_pattern = r"^\\+?[0-9\\-\\s]{10,}$"

for $phone in @phones {
    if $phone =~ $phone_pattern {
        print($phone + " - Valid")
    }
    if $phone !~ $phone_pattern {
        print($phone + " - Invalid")
    }
}''',
            category="regex",
            difficulty="medium"
        )
        
        # Password strength
        self._add_example(
            instruction="Check password strength with regex",
            input_code="Validate password meets complexity requirements",
            output_code='''# Password strength checker
$password = "SecureP@ss123"

$has_upper = r"[A-Z]"
$has_lower = r"[a-z]"
$has_digit = r"[0-9]"
$has_special = r"[!@#$%^&*]"

$strength = 0

if $password =~ $has_upper {
    $strength = $strength + 1
}
if $password =~ $has_lower {
    $strength = $strength + 1
}
if $password =~ $has_digit {
    $strength = $strength + 1
}
if $password =~ $has_special {
    $strength = $strength + 1
}
if &len($password) >= 8 {
    $strength = $strength + 1
}

print("Password strength: " + &str($strength) + "/5")''',
            category="regex",
            difficulty="hard"
        )
    
    # ========================================================================
    # VUE
    # ========================================================================
    
    def _generate_vue(self):
        """Generate Vue component examples"""
        
        # Basic Vue component
        self._add_example(
            instruction="Generate a Vue.js component from Pyrl",
            input_code="Create a UserCard Vue component with name, role, and avatar props",
            output_code='''# User data
%user_data = {
    "name": "John Doe",
    "role": "Administrator",
    "avatar": "https://example.com/avatar.jpg",
    "online": true
}

# Generate Vue component
vue "UserCard" {
    name: %user_data["name"],
    role: %user_data["role"],
    avatar: %user_data["avatar"],
    online: %user_data["online"]
}''',
            category="vue",
            difficulty="medium"
        )
        
        # Dashboard component
        self._add_example(
            instruction="Create a dashboard Vue component with statistics",
            input_code="Generate a StatsPanel Vue component with multiple statistics",
            output_code='''# Dashboard statistics
%stats = {
    "totalUsers": 1250,
    "activeUsers": 847,
    "revenue": 54230.50,
    "growth": 15.5
}

# Generate Vue dashboard component
vue "StatsPanel" {
    title: "Dashboard Overview",
    totalUsers: %stats["totalUsers"],
    activeUsers: %stats["activeUsers"],
    revenue: %stats["revenue"],
    growth: %stats["growth"]
}''',
            category="vue",
            difficulty="medium"
        )
    
    # ========================================================================
    # TESTING
    # ========================================================================
    
    def _generate_testing(self):
        """Generate test-related examples"""
        
        # Basic tests
        self._add_example(
            instruction="Write unit tests for a function",
            input_code="Create tests for an add function",
            output_code='''# Add function to test
&add($a, $b) = {
    return $a + $b
}

# Test suite
test "Add Function Tests" {
    # Test basic addition
    $result = &add(2, 3)
    assert $result == 5
    
    # Test with negative numbers
    $result = &add(-1, 1)
    assert $result == 0
    
    # Test with zero
    $result = &add(0, 0)
    assert $result == 0
}

print("All tests passed!")''',
            category="testing",
            difficulty="easy"
        )
        
        # Hash tests
        self._add_example(
            instruction="Write tests for hash operations",
            input_code="Create tests for a user management hash",
            output_code='''# User management hash
%users = {
    "alice": {"role": "admin", "active": true},
    "bob": {"role": "user", "active": false}
}

test "User Management Tests" {
    # Test user exists
    assert %users["alice"] != none
    
    # Test user role
    $alice_role = %users["alice"]["role"]
    assert $alice_role == "admin"
    
    # Test active status
    $bob_active = %users["bob"]["active"]
    assert $bob_active == false
    
    # Test adding new user
    %users["charlie"] = {"role": "user", "active": true}
    assert %users["charlie"] != none
}

print("User tests passed!")''',
            category="testing",
            difficulty="medium"
        )
    
    # ========================================================================
    # PLUGINS
    # ========================================================================
    
    def _generate_plugins(self):
        """Generate plugin-related examples"""
        
        # Using plugin functions
        self._add_example(
            instruction="Use extended math plugin functions",
            input_code="Calculate square root and trigonometric values",
            output_code='''# Math plugin functions (requires math_extended plugin)
$x = 16

# Square root
$sqrt_x = &sqrt($x)

# Trigonometry
$angle = 0.785398  # pi/4 radians (45 degrees)
$sin_val = &sin($angle)
$cos_val = &cos($angle)

# Constants
$pi = &pi()
$e = &e()

print("Square root of " + &str($x) + ": " + &str($sqrt_x))
print("sin(45°): " + &str($sin_val))
print("cos(45°): " + &str($cos_val))
print("Pi: " + &str($pi))
print("e: " + &str($e))''',
            category="plugins",
            difficulty="medium"
        )
        
        # DateTime plugin
        self._add_example(
            instruction="Work with dates using the datetime plugin",
            input_code="Format and manipulate dates",
            output_code='''# DateTime plugin functions (requires datetime plugin)
$now = &now()
$today = &today()

# Format date
$formatted = &format_date($now, "%Y-%m-%d %H:%M:%S")

# Add days
$future = &date_add($now, 7, 0, 0)  # Add 7 days

# Get timestamp
$ts = &timestamp()

print("Current datetime: " + $now)
print("Today: " + $today)
print("Formatted: " + $formatted)
print("7 days from now: " + $future)
print("Unix timestamp: " + &str($ts))''',
            category="plugins",
            difficulty="medium"
        )
    
    # ========================================================================
    # ALGORITHMS
    # ========================================================================
    
    def _generate_algorithms(self):
        """Generate algorithm examples"""
        
        # Binary search
        self._add_example(
            instruction="Implement binary search algorithm",
            input_code="Create a binary search function for sorted arrays",
            output_code='''# Binary search implementation
&binary_search(@arr, $target) = {
    $left = 0
    $right = &len(@arr) - 1
    
    while $left <= $right {
        $mid = &floor(($left + $right) / 2)
        $mid_val = @arr[$mid]
        
        if $mid_val == $target {
            return $mid
        }
        if $mid_val < $target {
            $left = $mid + 1
        }
        if $mid_val > $target {
            $right = $mid - 1
        }
    }
    
    return -1
}

# Test binary search
@sorted_nums = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
$index = &binary_search(@sorted_nums, 11)

print("Found 11 at index: " + &str($index))''',
            category="algorithms",
            difficulty="hard"
        )
        
        # Bubble sort
        self._add_example(
            instruction="Implement bubble sort algorithm",
            input_code="Sort an array using bubble sort",
            output_code='''# Bubble sort implementation
&bubble_sort(@arr) = {
    $n = &len(@arr)
    
    for $i in &range($n) {
        for $j in &range($n - $i - 1) {
            if @arr[$j] > @arr[$j + 1] {
                # Swap elements
                $temp = @arr[$j]
                @arr[$j] = @arr[$j + 1]
                @arr[$j + 1] = $temp
            }
        }
    }
    
    return @arr
}

# Test bubble sort
@numbers = [64, 34, 25, 12, 22, 11, 90]
@sorted = &bubble_sort(@numbers)

print("Sorted: " + &join(@sorted, ", "))''',
            category="algorithms",
            difficulty="hard"
        )
    
    # ========================================================================
    # WEB APP
    # ========================================================================
    
    def _generate_web_app(self):
        """Generate web application examples"""
        
        # Authentication system
        self._add_example(
            instruction="Create a simple authentication system",
            input_code="Implement user login with password validation",
            output_code='''# User database
%users = {
    "admin": {
        "password": "hashed_secret",
        "role": "administrator"
    },
    "user1": {
        "password": "hashed_pass",
        "role": "member"
    }
}

# Login function
&login($username, $password) = {
    $user = %users[$username]
    
    if $user == none {
        return "User not found"
    }
    
    $stored_pass = $user["password"]
    
    if $password == $stored_pass {
        return "Login successful"
    }
    
    return "Invalid password"
}

# Test login
$result = &login("admin", "hashed_secret")
print($result)''',
            category="web_app",
            difficulty="medium"
        )
        
        # Shopping cart
        self._add_example(
            instruction="Implement a shopping cart system",
            input_code="Create functions to manage a shopping cart",
            output_code='''# Shopping cart system
%cart = {}
$total = 0

# Add item to cart
&add_to_cart($item, $price, $quantity) = {
    %cart[$item] = {
        "price": $price,
        "quantity": $quantity
    }
}

# Calculate total
&calculate_total() = {
    $sum = 0
    @items = &keys(%cart)
    
    for $item in @items {
        $item_data = %cart[$item]
        $item_total = $item_data["price"] * $item_data["quantity"]
        $sum = $sum + $item_total
    }
    
    return $sum
}

# Add items
&add_to_cart("laptop", 999, 1)
&add_to_cart("mouse", 29, 2)
&add_to_cart("keyboard", 79, 1)

# Calculate and display
$total = &calculate_total()
print("Cart total: $" + &str($total))''',
            category="web_app",
            difficulty="medium"
        )
    
    # ========================================================================
    # OUTPUT
    # ========================================================================
    
    def to_jsonl(self, filepath: str):
        """Save examples to JSONL file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for ex in self.examples:
                record = {
                    "instruction": ex.instruction,
                    "input": ex.input,
                    "output": ex.output,
                    "category": ex.category,
                    "difficulty": ex.difficulty,
                    "metadata": ex.metadata or {}
                }
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    def to_json(self, filepath: str):
        """Save examples to JSON file"""
        data = []
        for ex in self.examples:
            data.append({
                "instruction": ex.instruction,
                "input": ex.input,
                "output": ex.output,
                "category": ex.category,
                "difficulty": ex.difficulty,
                "metadata": ex.metadata or {}
            })
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about generated examples"""
        categories = {}
        difficulties = {}
        
        for ex in self.examples:
            categories[ex.category] = categories.get(ex.category, 0) + 1
            difficulties[ex.difficulty] = difficulties.get(ex.difficulty, 0) + 1
        
        return {
            "total_examples": len(self.examples),
            "by_category": categories,
            "by_difficulty": difficulties
        }


def main():
    """Generate training data"""
    print("=" * 60)
    print("Pyrl Training Data Generator")
    print("=" * 60)
    
    generator = PyrlDataGenerator()
    examples = generator.generate_all()
    
    # Print statistics
    stats = generator.get_statistics()
    print(f"\nGenerated {stats['total_examples']} examples")
    print("\nBy Category:")
    for cat, count in stats['by_category'].items():
        print(f"  {cat}: {count}")
    
    print("\nBy Difficulty:")
    for diff, count in stats['by_difficulty'].items():
        print(f"  {diff}: {count}")
    
    # Save to files
    output_dir = os.path.dirname(__file__)
    jsonl_path = os.path.join(output_dir, "dataset.jsonl")
    json_path = os.path.join(output_dir, "dataset.json")
    
    generator.to_jsonl(jsonl_path)
    generator.to_json(json_path)
    
    print(f"\nSaved to:")
    print(f"  JSONL: {jsonl_path}")
    print(f"  JSON: {json_path}")


if __name__ == "__main__":
    main()
