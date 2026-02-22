# FILE: pyrl_ai.py
"""
Pyrl AI Assistant
AI-powered code generation and intelligent assistance for Pyrl language

Version: 1.0.0
Author: Pyrl Ecosystem Team

Features:
- Code generation from natural language
- Code completion and suggestion
- Plugin discovery and auto-loading
- Intelligent error fixing
- Code explanation and documentation
"""

import json
import re
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Import Pyrl components
try:
    from pyrl_vm import PyrlVM, PyrlSyntaxError, PyrlRuntimeError
    from pyrl_plugin_system import PluginManager, load_builtin_plugins, PluginBase
except ImportError:
    # For standalone usage
    pass


class TaskType(Enum):
    """Types of tasks the AI can perform"""
    GENERATE_CODE = "generate_code"
    EXPLAIN_CODE = "explain_code"
    FIX_ERROR = "fix_error"
    COMPLETE_CODE = "complete_code"
    SUGGEST_PLUGIN = "suggest_plugin"
    CREATE_PLUGIN = "create_plugin"


@dataclass
class CodeContext:
    """Context for code generation"""
    task_type: TaskType
    prompt: str
    existing_code: str = ""
    error_message: str = ""
    target_category: str = ""
    difficulty: str = "medium"


@dataclass
class GenerationResult:
    """Result of AI generation"""
    success: bool
    code: str = ""
    explanation: str = ""
    suggestions: List[str] = field(default_factory=list)
    plugins_needed: List[str] = field(default_factory=list)
    confidence: float = 0.0


class PyrlKnowledgeBase:
    """Knowledge base for Pyrl language patterns and examples"""
    
    def __init__(self):
        self.patterns = self._init_patterns()
        self.examples = self._init_examples()
        self.snippets = self._init_snippets()
    
    def _init_patterns(self) -> Dict[str, Any]:
        """Initialize code patterns"""
        return {
            "variable_scalar": {
                "template": "$name = {value}",
                "sigil": "$",
                "description": "Scalar variable for single values"
            },
            "variable_array": {
                "template": "@name = [{items}]",
                "sigil": "@",
                "description": "Array variable for ordered lists"
            },
            "variable_hash": {
                "template": "%name = {{ {items} }}",
                "sigil": "%",
                "description": "Hash variable for key-value pairs"
            },
            "function": {
                "template": "&name($params) = {{ {body} }}",
                "sigil": "&",
                "description": "Function definition"
            },
            "conditional": {
                "template": "if {condition} {{ {body} }}",
                "description": "Conditional execution"
            },
            "loop_for": {
                "template": "for $var in {iterable} {{ {body} }}",
                "description": "For loop iteration"
            },
            "loop_while": {
                "template": "while {condition} {{ {body} }}",
                "description": "While loop"
            },
            "test_block": {
                "template": "test \"{name}\" {{ {body} }}",
                "description": "Test block definition"
            },
            "vue_component": {
                "template": "vue \"{name}\" {{ {props} }}",
                "description": "Vue component generation"
            },
            "regex_match": {
                "template": "{string} =~ {pattern}",
                "description": "Regex match operation"
            },
            "assertion": {
                "template": "assert {left} {op} {right}",
                "description": "Test assertion"
            }
        }
    
    def _init_examples(self) -> List[Dict[str, str]]:
        """Initialize example code snippets"""
        return [
            {
                "category": "variables",
                "description": "scalar variable declaration",
                "code": '$name = "John"\n$age = 25\n$active = true'
            },
            {
                "category": "arrays",
                "description": "array operations",
                "code": '@items = [1, 2, 3, 4, 5]\n&push(@items, 6)\n$last = &pop(@items)'
            },
            {
                "category": "hashes",
                "description": "hash creation and access",
                "code": '%user = {"name": "Alice", "age": 30}\n$name = %user["name"]'
            },
            {
                "category": "functions",
                "description": "function definition",
                "code": '&add($a, $b) = {\n    return $a + $b\n}'
            },
            {
                "category": "conditionals",
                "description": "if-else logic",
                "code": 'if $x > 0 {\n    print("positive")\n}\nif $x < 0 {\n    print("negative")\n}'
            },
            {
                "category": "loops",
                "description": "for loop iteration",
                "code": 'for $i in @items {\n    print($i)\n}'
            },
            {
                "category": "regex",
                "description": "pattern matching",
                "code": '$email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"\nif $email =~ $email_pattern {\n    print("valid")\n}'
            },
            {
                "category": "testing",
                "description": "test block",
                "code": 'test "Math operations" {\n    $result = &add(2, 3)\n    assert $result == 5\n}'
            }
        ]
    
    def _init_snippets(self) -> Dict[str, str]:
        """Initialize code snippets for common tasks"""
        return {
            "function": '''&{name}({params}) = {{
    {body}
}}''',
            "test": '''test "{name}" {{
    {body}
}}''',
            "class_like": '''# {name} module
%{name}_data = {{}}

&{name}_create({params}) = {{
    %{name}_data["id"] = &uuid()
    %{name}_data["created"] = &now()
    return %{name}_data
}}

&{name}_get($id) = {{
    return %{name}_data[$id]
}}''',
            "crud": '''# CRUD operations for {name}
%{name}s = {{}}

&create_{name}($data) = {{
    $id = &uuid()
    %{name}s[$id] = $data
    return $id
}}

&get_{name}($id) = {{
    return %{name}s[$id]
}}

&update_{name}($id, $data) = {{
    %{name}s[$id] = $data
    return true
}}

&delete_{name}($id) = {{
    %{name}s[$id] = none
    return true
}}

&list_{name}s() = {{
    return &values(%{name}s})
}}''',
            "validation": '''# Validation function
&validate_{name}($data) = {{
    $errors = []
    
    if &len($data["name"]) == 0 {{
        &push($errors, "Name is required")
    }}
    
    if $data["email"] !~ r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$" {{
        &push($errors, "Invalid email format")
    }}
    
    return $errors
}}'''
        }
    
    def find_similar_examples(self, description: str) -> List[Dict[str, str]]:
        """Find examples similar to the description"""
        keywords = description.lower().split()
        results = []
        
        for example in self.examples:
            score = 0
            example_desc = example["description"].lower()
            
            for keyword in keywords:
                if keyword in example_desc or keyword in example["category"]:
                    score += 1
            
            if score > 0:
                results.append({**example, "relevance": score})
        
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:3]


class PyrlAI:
    """AI assistant for Pyrl code generation and assistance"""
    
    def __init__(self, vm=None, use_plugins: bool = True):
        self.vm = vm or PyrlVM()
        self.knowledge = PyrlKnowledgeBase()
        self.context_history: List[Dict[str, Any]] = []
        
        # Initialize plugin system
        if use_plugins:
            self.plugin_manager = PluginManager(self.vm)
            load_builtin_plugins(self.plugin_manager)
        else:
            self.plugin_manager = None
        
        # LLM integration placeholder
        self.llm_client = None
        self.model_name = "pyrl-assistant-v1"
    
    # ========================================================================
    # LLM INTEGRATION
    # ========================================================================
    
    def set_llm_client(self, client):
        """Set LLM client for advanced features"""
        self.llm_client = client
    
    def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """Call the LLM with a prompt"""
        if self.llm_client:
            try:
                # This is a placeholder for actual LLM integration
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt or "You are a Pyrl language expert."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"LLM error: {e}")
        
        # Fallback to template-based generation
        return self._template_generate(prompt)
    
    def _template_generate(self, prompt: str) -> str:
        """Template-based code generation (fallback)"""
        prompt_lower = prompt.lower()
        
        # Detect task type from prompt
        if "function" in prompt_lower or "create" in prompt_lower:
            return self._generate_function_from_prompt(prompt)
        elif "test" in prompt_lower:
            return self._generate_test_from_prompt(prompt)
        elif "hash" in prompt_lower or "dictionary" in prompt_lower:
            return self._generate_hash_from_prompt(prompt)
        elif "array" in prompt_lower or "list" in prompt_lower:
            return self._generate_array_from_prompt(prompt)
        elif "vue" in prompt_lower or "component" in prompt_lower:
            return self._generate_vue_from_prompt(prompt)
        else:
            return self._generate_generic_from_prompt(prompt)
    
    # ========================================================================
    # CODE GENERATION
    # ========================================================================
    
    def generate_code(self, prompt: str, context: CodeContext = None) -> GenerationResult:
        """Generate Pyrl code from natural language prompt"""
        if context is None:
            context = CodeContext(
                task_type=TaskType.GENERATE_CODE,
                prompt=prompt
            )
        
        # Find similar examples
        similar = self.knowledge.find_similar_examples(prompt)
        
        # Generate code
        system_prompt = self._build_system_prompt(context, similar)
        generated = self._call_llm(prompt, system_prompt)
        
        # Validate generated code
        is_valid, errors = self._validate_code(generated)
        
        # Detect needed plugins
        plugins = self._detect_required_plugins(generated)
        
        result = GenerationResult(
            success=is_valid,
            code=generated,
            explanation=self._explain_generated_code(generated),
            suggestions=self._generate_suggestions(generated),
            plugins_needed=plugins,
            confidence=0.85 if is_valid else 0.5
        )
        
        # Store in context history
        self.context_history.append({
            "prompt": prompt,
            "result": result,
            "context": context
        })
        
        return result
    
    def _build_system_prompt(self, context: CodeContext, examples: List[Dict]) -> str:
        """Build system prompt for LLM"""
        prompt = """You are an expert in the Pyrl programming language.

Pyrl is a hybrid Python-Perl inspired language with the following features:
- Sigil-based variables: $scalar, @array, %hash, &function
- Regex operators: =~ (match), !~ (not match)
- Built-in functions: &len, &str, &int, &upper, &lower, &push, &pop, &keys, &values
- Vue.js 3 component generation
- Built-in test framework with assert statements

Generate clean, idiomatic Pyrl code following these conventions:
1. Use appropriate sigils for variable types
2. Follow consistent indentation (4 spaces)
3. Include comments for complex logic
4. Use meaningful variable names
5. Prefer built-in functions where available

"""
        
        if examples:
            prompt += "\nRelevant examples:\n"
            for ex in examples:
                prompt += f"\n# {ex['description']}\n{ex['code']}\n"
        
        return prompt
    
    def _generate_function_from_prompt(self, prompt: str) -> str:
        """Generate a function from prompt"""
        # Extract function name if present
        name_match = re.search(r'(?:function|func)\s+(\w+)', prompt, re.IGNORECASE)
        func_name = name_match.group(1) if name_match else "generated_func"
        
        # Extract parameters if present
        params_match = re.search(r'parameter[s]?\s+(?:are|:)?\s*([^\n]+)', prompt, re.IGNORECASE)
        params = []
        if params_match:
            params = [p.strip() for p in params_match.group(1).split(',')]
        
        params_str = ", ".join([f"${p}" for p in params]) if params else "$input"
        
        # Generate function based on prompt intent
        if "add" in prompt.lower() or "sum" in prompt.lower():
            return f'''&{func_name}($a, $b) = {{
    return $a + $b
}}'''
        elif "calculate" in prompt.lower():
            return f'''&{func_name}({params_str}) = {{
    # Calculate result
    $result = $input
    return $result
}}'''
        else:
            return f'''&{func_name}({params_str}) = {{
    # TODO: Implement logic
    return $input
}}'''
    
    def _generate_test_from_prompt(self, prompt: str) -> str:
        """Generate test code from prompt"""
        # Extract test name
        name_match = re.search(r'test\s+(?:for\s+)?(\w+)', prompt, re.IGNORECASE)
        test_name = name_match.group(1) if name_match else "GeneratedTest"
        
        return f'''test "{test_name}" {{
    # Setup
    $input = "test_value"
    
    # Execute
    $result = $input
    
    # Assert
    assert $result != none
    assert &len($result) > 0
}}'''
    
    def _generate_hash_from_prompt(self, prompt: str) -> str:
        """Generate hash code from prompt"""
        return '''%data = {
    "key1": "value1",
    "key2": "value2",
    "nested": {
        "inner_key": "inner_value"
    }
}

# Access values
$value = %data["key1"]
$nested = %data["nested"]["inner_key"]'''
    
    def _generate_array_from_prompt(self, prompt: str) -> str:
        """Generate array code from prompt"""
        return '''@items = [1, 2, 3, 4, 5]

# Array operations
&push(@items, 6)
$last = &pop(@items)
$first = @items[0]
$count = &len(@items)

# Iteration
for $item in @items {
    print($item)
}'''
    
    def _generate_vue_from_prompt(self, prompt: str) -> str:
        """Generate Vue component from prompt"""
        # Extract component name
        name_match = re.search(r'(?:component|vue)\s+(\w+)', prompt, re.IGNORECASE)
        comp_name = name_match.group(1) if name_match else "MyComponent"
        
        return f'''vue "{comp_name}" {{
    title: "Welcome",
    description: "A generated component",
    count: 0
}}'''
    
    def _generate_generic_from_prompt(self, prompt: str) -> str:
        """Generate generic code from prompt"""
        return f'''# Generated Pyrl code
# Prompt: {prompt}

$result = "Generated based on prompt"

print($result)'''
    
    # ========================================================================
    # CODE VALIDATION
    # ========================================================================
    
    def _validate_code(self, code: str) -> Tuple[bool, List[str]]:
        """Validate Pyrl code"""
        errors = []
        
        try:
            # Try to parse the code
            self.vm.parser.parse(code)
            
            # Try to execute (dry run)
            self.vm.reset()
            # Note: We don't actually execute to avoid side effects
            
            return True, []
            
        except PyrlSyntaxError as e:
            errors.append(f"Syntax error: {str(e)}")
            return False, errors
            
        except Exception as e:
            errors.append(f"Error: {str(e)}")
            return False, errors
    
    def _detect_required_plugins(self, code: str) -> List[str]:
        """Detect which plugins are needed for the code"""
        plugins = []
        
        plugin_signatures = {
            "math_extended": ["&sqrt", "&pow", "&sin", "&cos", "&tan", "&pi", "&e", "&floor", "&ceil"],
            "datetime": ["&now", "&today", "&format_date", "&parse_date", "&date_add", "&timestamp"],
            "http_client": ["&http_get", "&http_post", "&http_put", "&http_delete"],
            "crypto": ["&md5", "&sha1", "&sha256", "&base64_encode", "&base64_decode", "&uuid"]
        }
        
        for plugin_name, functions in plugin_signatures.items():
            for func in functions:
                if func in code:
                    if plugin_name not in plugins:
                        plugins.append(plugin_name)
                    break
        
        return plugins
    
    # ========================================================================
    # CODE EXPLANATION
    # ========================================================================
    
    def explain_code(self, code: str) -> str:
        """Explain what the code does"""
        lines = code.strip().split('\n')
        explanations = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Variable assignments
            if '=' in line and not line.startswith('if') and not line.startswith('while'):
                if line.startswith('$'):
                    explanations.append(f"- Scalar variable assignment: {line.split('=')[0].strip()}")
                elif line.startswith('@'):
                    explanations.append(f"- Array variable assignment: {line.split('=')[0].strip()}")
                elif line.startswith('%'):
                    explanations.append(f"- Hash variable assignment: {line.split('=')[0].strip()}")
            
            # Function definition
            if line.startswith('&') and '=' in line:
                func_name = line.split('(')[0].strip()
                explanations.append(f"- Function definition: {func_name}")
            
            # Conditionals
            if line.startswith('if '):
                explanations.append(f"- Conditional check")
            
            # Loops
            if line.startswith('for '):
                explanations.append(f"- For loop iteration")
            elif line.startswith('while '):
                explanations.append(f"- While loop")
            
            # Function calls
            if '&' in line and '(' in line:
                func_calls = re.findall(r'&(\w+)\(', line)
                for func in func_calls:
                    explanations.append(f"- Function call: &{func}")
            
            # Test blocks
            if line.startswith('test '):
                explanations.append(f"- Test block definition")
            
            # Vue components
            if line.startswith('vue '):
                explanations.append(f"- Vue component generation")
        
        if explanations:
            return "This code:\n" + "\n".join(explanations)
        return "Unable to explain this code."
    
    def _explain_generated_code(self, code: str) -> str:
        """Generate explanation for generated code"""
        return self.explain_code(code)
    
    # ========================================================================
    # ERROR FIXING
    # ========================================================================
    
    def fix_error(self, code: str, error_message: str) -> GenerationResult:
        """Attempt to fix code errors"""
        fixed_code = code
        fixes_applied = []
        
        # Common error patterns and fixes
        error_fixes = [
            # Missing sigil
            (r'(\w+)\s*=\s*', r'$\1 = ', "Added missing scalar sigil"),
            # Wrong brackets for hash access
            (r'%(\w+)\s*\{\s*"?(\w+)"?\s*\}', r'%\1["\2"]', "Fixed hash access syntax"),
            # Missing function sigil
            (r'def\s+(\w+)', r'&\1', "Added function sigil"),
            # Python-style boolean
            (r'\bTrue\b', r'true', "Fixed boolean capitalization"),
            (r'\bFalse\b', r'false', "Fixed boolean capitalization"),
            (r'\bNone\b', r'none', "Fixed None capitalization"),
        ]
        
        for pattern, replacement, fix_desc in error_fixes:
            new_code = re.sub(pattern, replacement, fixed_code)
            if new_code != fixed_code:
                fixed_code = new_code
                fixes_applied.append(fix_desc)
        
        # Validate fixed code
        is_valid, errors = self._validate_code(fixed_code)
        
        return GenerationResult(
            success=is_valid,
            code=fixed_code,
            explanation=f"Applied fixes: {', '.join(fixes_applied)}" if fixes_applied else "No automatic fixes available",
            suggestions=errors if not is_valid else [],
            confidence=0.9 if is_valid else 0.5
        )
    
    # ========================================================================
    # CODE COMPLETION
    # ========================================================================
    
    def complete_code(self, partial_code: str) -> List[str]:
        """Suggest code completions"""
        suggestions = []
        lines = partial_code.strip().split('\n')
        last_line = lines[-1] if lines else ""
        
        # Variable completions
        if last_line.strip().startswith('$'):
            # Extract variable name
            var_match = re.match(r'\$(\w*)', last_line.strip())
            if var_match:
                prefix = var_match.group(1)
                # Suggest common operations
                suggestions.append(f"${prefix} = ")  # Assignment
                suggestions.append(f"${prefix} + ")  # Addition
        
        # Function call completions
        if '&' in last_line:
            func_match = re.search(r'&(\w*)$', last_line)
            if func_match:
                prefix = func_match.group(1)
                builtin_funcs = ['len', 'str', 'int', 'upper', 'lower', 'trim', 'split', 'join', 'push', 'pop', 'keys', 'values']
                for func in builtin_funcs:
                    if func.startswith(prefix):
                        suggestions.append(f"&{func}(")
        
        # Block completions
        if last_line.strip().endswith('{'):
            suggestions.append("    # code here\n}")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    # ========================================================================
    # PLUGIN SUGGESTIONS
    # ========================================================================
    
    def suggest_plugins(self, code: str) -> List[Dict[str, str]]:
        """Suggest plugins that could enhance the code"""
        suggestions = []
        
        # Check for math operations
        if any(op in code for op in ['**', 'sqrt', 'sin', 'cos', 'log']):
            suggestions.append({
                "plugin": "math_extended",
                "reason": "Provides advanced math functions like sqrt, sin, cos, pow",
                "functions": ["&sqrt", "&pow", "&sin", "&cos", "&tan", "&pi", "&e"]
            })
        
        # Check for date operations
        if any(word in code.lower() for word in ['date', 'time', 'now', 'today', 'timestamp']):
            suggestions.append({
                "plugin": "datetime",
                "reason": "Provides date and time manipulation functions",
                "functions": ["&now", "&today", "&format_date", "&date_add", "&timestamp"]
            })
        
        # Check for HTTP operations
        if any(word in code.lower() for word in ['http', 'fetch', 'api', 'request', 'url']):
            suggestions.append({
                "plugin": "http_client",
                "reason": "Provides HTTP client functions for API calls",
                "functions": ["&http_get", "&http_post", "&http_put", "&http_delete"]
            })
        
        # Check for security operations
        if any(word in code.lower() for word in ['hash', 'encrypt', 'password', 'token', 'uuid']):
            suggestions.append({
                "plugin": "crypto",
                "reason": "Provides cryptographic and hashing functions",
                "functions": ["&md5", "&sha256", "&uuid", "&base64_encode", "&random_string"]
            })
        
        return suggestions
    
    def _generate_suggestions(self, code: str) -> List[str]:
        """Generate improvement suggestions for code"""
        suggestions = []
        
        # Check for missing error handling
        if 'assert' in code and 'try' not in code:
            suggestions.append("Consider adding error handling around assertions")
        
        # Check for magic numbers
        if re.search(r'\b\d{2,}\b', code) and not re.search(r'#.*\d', code):
            suggestions.append("Consider documenting magic numbers with comments")
        
        # Check for repeated code
        lines = [l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('#')]
        if len(lines) != len(set(lines)):
            suggestions.append("Consider extracting repeated code into a function")
        
        return suggestions[:3]
    
    # ========================================================================
    # PLUGIN CREATION
    # ========================================================================
    
    def create_plugin(self, name: str, description: str, functions: List[Dict[str, str]]) -> str:
        """Generate a new plugin from specification"""
        plugin_code = f'''# FILE: plugin.py
"""
{name} Plugin
{description}

Auto-generated by Pyrl AI Assistant
"""

from pyrl_plugin_system import PluginBase


class {name.replace('_', '').title()}Plugin(PluginBase):
    """Plugin: {name}"""
    
    NAME = "{name}"
    VERSION = "1.0.0"
    DESCRIPTION = """{description}"""
    AUTHOR = "Pyrl AI Assistant"
    
    def on_load(self):
        # Register plugin functions
'''
        
        for func in functions:
            func_name = func.get('name', 'function')
            func_desc = func.get('description', '')
            func_params = func.get('params', [])
            func_body = func.get('body', 'pass')
            
            params_str = ', '.join(func_params) if func_params else ''
            
            plugin_code += f'''        self.register_function("{func_name}", self._{func_name})
    
    def _{func_name}(self, {params_str}):
        """{func_desc}"""
        {func_body}
'''
        
        return plugin_code
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get generation history"""
        return self.context_history[-limit:]
    
    def clear_history(self):
        """Clear generation history"""
        self.context_history = []
    
    def execute_code(self, code: str) -> Any:
        """Execute Pyrl code and return result"""
        try:
            return self.vm.execute(code)
        except Exception as e:
            return f"Execution error: {str(e)}"
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin by name"""
        if self.plugin_manager:
            return self.plugin_manager.load_plugin(plugin_name)
        return False


# ============================================================================
# INTERACTIVE SESSION
# ============================================================================

class PyrlInteractiveSession:
    """Interactive session for Pyrl AI Assistant"""
    
    def __init__(self, ai: PyrlAI = None):
        self.ai = ai or PyrlAI()
        self.history: List[Dict[str, Any]] = []
    
    def process_input(self, user_input: str) -> str:
        """Process user input and return response"""
        user_input = user_input.strip()
        
        # Command detection
        if user_input.startswith('/'):
            return self._handle_command(user_input)
        
        # Code generation request
        result = self.ai.generate_code(user_input)
        
        response = f"Generated Code:\n```\n{result.code}\n```\n"
        
        if result.explanation:
            response += f"\nExplanation:\n{result.explanation}\n"
        
        if result.plugins_needed:
            response += f"\nRequired Plugins: {', '.join(result.plugins_needed)}\n"
        
        if result.suggestions:
            response += f"\nSuggestions:\n- " + "\n- ".join(result.suggestions) + "\n"
        
        return response
    
    def _handle_command(self, command: str) -> str:
        """Handle slash commands"""
        cmd_parts = command.split()
        cmd = cmd_parts[0].lower()
        
        if cmd == '/help':
            return self._show_help()
        elif cmd == '/run':
            code = ' '.join(cmd_parts[1:])
            result = self.ai.execute_code(code)
            return f"Result: {result}"
        elif cmd == '/explain':
            code = ' '.join(cmd_parts[1:])
            return self.ai.explain_code(code)
        elif cmd == '/fix':
            # Read code from next lines
            return "Paste the code to fix (not implemented in this mode)"
        elif cmd == '/plugins':
            if self.ai.plugin_manager:
                plugins = self.ai.plugin_manager.list_plugins()
                if plugins:
                    return "Available plugins:\n" + "\n".join([f"  - {p.name} v{p.version}" for p in plugins])
                return "No plugins loaded"
            return "Plugin system not initialized"
        elif cmd == '/history':
            history = self.ai.get_history(5)
            return f"Recent generations: {len(history)}"
        elif cmd == '/clear':
            self.ai.clear_history()
            return "History cleared"
        else:
            return f"Unknown command: {cmd}\nType /help for available commands"
    
    def _show_help(self) -> str:
        """Show help message"""
        return """
Pyrl AI Assistant Commands:
===========================
<description>  - Generate Pyrl code from description
/run <code>    - Execute Pyrl code directly
/explain <code> - Explain what the code does
/fix           - Fix code errors (interactive)
/plugins       - List available plugins
/history       - Show recent generations
/clear         - Clear generation history
/help          - Show this help message

Examples:
- "Create a function to calculate factorial"
- "Generate a test for user authentication"
- "Make a Vue component for user profile"
"""


def main():
    """Main entry point"""
    print("=" * 60)
    print("Pyrl AI Assistant v1.0.0")
    print("=" * 60)
    
    # Initialize AI
    ai = PyrlAI()
    
    # Show available plugins
    if ai.plugin_manager:
        print("\nLoaded plugins:")
        for plugin in ai.plugin_manager.list_plugins():
            print(f"  - {plugin.name} v{plugin.version}: {plugin.description}")
    
    # Test generation
    print("\n" + "=" * 60)
    print("Test: Generate a function to add two numbers")
    print("=" * 60)
    
    result = ai.generate_code("Create a function to add two numbers")
    print(result.code)
    
    print("\n" + "=" * 60)
    print("Test: Generate a test block")
    print("=" * 60)
    
    result = ai.generate_code("Create a test for a multiply function")
    print(result.code)
    
    print("\n" + "=" * 60)
    print("Test: Execute code")
    print("=" * 60)
    
    exec_result = ai.execute_code('''
$name = "World"
$greeting = "Hello, " + $name + "!"
print($greeting)
''')
    print(f"Execution result: {exec_result}")


if __name__ == "__main__":
    main()
