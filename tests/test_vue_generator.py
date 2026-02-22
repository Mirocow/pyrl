# FILE: tests/test_vue_generator.py
"""
Comprehensive tests for Vue component generation
Tests: generate_vue_component function
"""

import pytest
from pyrl_vm import generate_vue_component, PyrlVM


class TestVueGenerator:
    """Test Vue component generation"""
    
    def test_basic_component(self):
        """Test basic component generation"""
        result = generate_vue_component("TestComponent", {})
        
        assert '<template>' in result
        assert '</template>' in result
        assert '<script setup>' in result
        assert '</script>' in result
        assert '<style scoped>' in result
        assert '</style>' in result
    
    def test_component_name_in_template(self):
        """Test component name appears in template"""
        result = generate_vue_component("MyCard", {})
        
        assert 'my-card-component' in result
        assert 'MyCard Component' in result
    
    def test_string_prop(self):
        """Test string prop handling"""
        result = generate_vue_component("User", {"name": "Alice"})
        
        assert "name" in result
        assert "Alice" in result
        assert "ref('Alice')" in result
    
    def test_number_prop(self):
        """Test number prop handling"""
        result = generate_vue_component("Counter", {"count": 42})
        
        assert "count" in result
        assert "42" in result
    
    def test_boolean_prop_true(self):
        """Test boolean true prop handling"""
        result = generate_vue_component("Toggle", {"active": True})
        
        assert "active" in result
        assert "'Yes'" in result
    
    def test_boolean_prop_false(self):
        """Test boolean false prop handling"""
        result = generate_vue_component("Toggle", {"active": False})
        
        assert "active" in result
        assert "'No'" in result
    
    def test_array_prop(self):
        """Test array prop handling"""
        result = generate_vue_component("List", {"items": [1, 2, 3]})
        
        assert "items" in result
        assert "v-for" in result
        assert "[1, 2, 3]" in result
    
    def test_dict_prop(self):
        """Test dict prop handling"""
        result = generate_vue_component("Profile", {"user": {"name": "Bob"}})
        
        assert "user" in result
        assert "v-for" in result
    
    def test_none_prop(self):
        """Test null prop handling"""
        result = generate_vue_component("Empty", {"value": None})
        
        assert "value" in result
        assert "ref(null)" in result
    
    def test_multiple_props(self):
        """Test multiple props"""
        props = {
            "name": "Alice",
            "age": 30,
            "active": True
        }
        result = generate_vue_component("User", props)
        
        assert "name" in result
        assert "Alice" in result
        assert "age" in result
        assert "30" in result
        assert "active" in result
    
    def test_style_scoped(self):
        """Test style is scoped"""
        result = generate_vue_component("Card", {})
        
        assert '<style scoped>' in result
        assert '.card-component' in result
    
    def test_vue_import(self):
        """Test Vue imports"""
        result = generate_vue_component("Test", {})
        
        assert "import { ref, computed } from 'vue'" in result
    
    def test_lowercase_component_name(self):
        """Test component name lowercase in class"""
        result = generate_vue_component("MyAwesomeComponent", {})
        
        assert 'my-awesome-component' in result


class TestVueExecution:
    """Test Vue generation through VM execution"""
    
    @pytest.fixture
    def vm(self):
        """Create a fresh VM"""
        return PyrlVM()
    
    def test_vue_basic_execution(self, vm):
        """Test basic Vue generation through VM"""
        result = vm.execute('vue "Card" { }')
        
        assert '<template>' in result
        assert 'Card' in result
    
    def test_vue_with_props_execution(self, vm):
        """Test Vue with props through VM"""
        result = vm.execute('vue "User" { name: "Alice", age: 30 }')
        
        assert 'name' in result
        assert 'Alice' in result
    
    def test_vue_with_variable_props(self, vm):
        """Test Vue with variable props"""
        vm.execute('$title = "Hello World"')
        result = vm.execute('vue "Header" { title: $title }')
        
        assert 'Hello World' in result
    
    def test_vue_with_expression_props(self, vm):
        """Test Vue with expression props"""
        result = vm.execute('vue "Math" { result: 5 + 5 }')
        
        assert '10' in result
    
    def test_vue_with_array_prop(self, vm):
        """Test Vue with array prop"""
        vm.execute('@items = [1, 2, 3]')
        result = vm.execute('vue "List" { items: @items }')
        
        assert 'v-for' in result
    
    def test_vue_with_hash_prop(self, vm):
        """Test Vue with hash prop"""
        vm.execute('%user = {"name": "Bob", "email": "bob@test.com"}')
        result = vm.execute('vue "Profile" { user: %user }')
        
        assert 'user' in result


class TestVuePropTypes:
    """Test different prop types in Vue generation"""
    
    def test_float_prop(self):
        """Test float prop"""
        result = generate_vue_component("Decimal", {"value": 3.14})
        
        assert "3.14" in result
    
    def test_negative_number_prop(self):
        """Test negative number prop"""
        result = generate_vue_component("Negative", {"value": -42})
        
        assert "-42" in result
    
    def test_empty_array_prop(self):
        """Test empty array prop"""
        result = generate_vue_component("EmptyList", {"items": []})
        
        assert "[]" in result
    
    def test_empty_dict_prop(self):
        """Test empty dict prop"""
        result = generate_vue_component("EmptyObj", {"data": {}})
        
        assert "{}" in result
    
    def test_nested_dict_prop(self):
        """Test nested dict prop"""
        nested = {"outer": {"inner": "value"}}
        result = generate_vue_component("Nested", {"data": nested})
        
        assert "v-for" in result


class TestVueOutputFormat:
    """Test Vue output format"""
    
    def test_output_is_string(self):
        """Test output is string"""
        result = generate_vue_component("Test", {})
        assert isinstance(result, str)
    
    def test_template_section_exists(self):
        """Test template section exists"""
        result = generate_vue_component("Test", {})
        
        template_start = result.find('<template>')
        template_end = result.find('</template>')
        assert template_start < template_end
    
    def test_script_section_exists(self):
        """Test script section exists"""
        result = generate_vue_component("Test", {})
        
        script_start = result.find('<script setup>')
        script_end = result.find('</script>')
        assert script_start < script_end
    
    def test_style_section_exists(self):
        """Test style section exists"""
        result = generate_vue_component("Test", {})
        
        style_start = result.find('<style scoped>')
        style_end = result.find('</style>')
        assert style_start < style_end
    
    def test_sections_in_order(self):
        """Test sections are in correct order"""
        result = generate_vue_component("Test", {})
        
        template_pos = result.find('<template>')
        script_pos = result.find('<script setup>')
        style_pos = result.find('<style scoped>')
        
        assert template_pos < script_pos < style_pos
