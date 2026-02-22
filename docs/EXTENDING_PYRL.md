# Как расширить Pyrl: Полное руководство

## Архитектура расширения Pyrl

Pyrl поддерживает два уровня расширения:

### Уровень 1: Плагины (Runtime Extension)
Плагины добавляют новые функции и возможности БЕЗ изменения синтаксиса.

### Уровень 2: Расширение грамматики (Language Extension)
Добавление новых синтаксических конструкций требует изменения парсера.

---

## Процесс добавления OOP (Классов)

### Шаг 1: Определение синтаксиса

```pyrl
# Определяем синтаксис классов в стиле Pyrl
class User {
    # Конструктор
    init($name, $email) = {
        @self.name = $name
        @self.email = $email
    }
    
    # Метод
    greet() = {
        return "Hello, " + @self.name
    }
    
    # Геттер
    get_email() = {
        return @self.email
    }
}

# Создание экземпляра
$user = User("Alice", "alice@example.com")

# Вызов метода
$greeting = $user.greet()
```

### Шаг 2: Расширение грамматики

Добавляем в Lark гRAMMAR новые правила:

```python
# Новые правила грамматики
class_definition: "class" IDENT class_body
class_body: "{" class_member* "}"
class_member: method_definition | property_definition
method_definition: "method" IDENT "(" [param_list] ")" "=" block
init_definition: "init" "(" [param_list] ")" "=" block
instance_creation: IDENT "(" [arg_list] ")"
method_call: primary_expr "." IDENT "(" [arg_list] ")"
```

### Шаг 3: Создание AST узлов

```python
@dataclass
class ClassDefNode(ASTNode):
    name: str
    methods: Dict[str, 'FunctionDefNode']
    properties: Dict[str, ASTNode]
    
@dataclass
class InstanceCreationNode(ASTNode):
    class_name: str
    args: List[ASTNode]

@dataclass
class MethodCallNode(ASTNode):
    instance: ASTNode
    method_name: str
    args: List[ASTNode]
```

### Шаг 4: Реализация в интерпретаторе

```python
def execute_ClassDefNode(self, node):
    # Регистрируем класс как фабрику
    classdef = PyrlClass(node.name, node.methods, node.properties)
    self.vm.register_class(node.name, classdef)
    
def execute_InstanceCreationNode(self, node):
    # Создаем экземпляр класса
    classdef = self.vm.get_class(node.class_name)
    instance = classdef.create_instance()
    # Вызываем init
    if 'init' in classdef.methods:
        args = [self.execute(arg) for arg in node.args]
        classdef.methods['init'](instance, *args)
    return instance
```

---

## Диаграмма процесса расширения

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYRL EXTENSION PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DESIGN PHASE                                                │
│     ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│     │ Define       │ -> │ Design       │ -> │ Plan AST     │   │
│     │ Syntax       │    │ Grammar      │    │ Nodes        │   │
│     └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                                 │
│  2. IMPLEMENTATION PHASE                                        │
│     ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│     │ Update       │ -> │ Add AST      │ -> │ Update       │   │
│     │ Grammar      │    │ Nodes        │    │ Interpreter  │   │
│     └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                                 │
│  3. INTEGRATION PHASE                                           │
│     ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│     │ Create       │ -> │ Write        │ -> │ Test &       │   │
│     │ Plugin       │    │ Examples     │    │ Validate     │   │
│     └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                                 │
│  4. TRAINING PHASE                                              │
│     ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│     │ Generate     │ -> │ Update       │ -> │ Fine-tune    │   │
│     │ Dataset      │    │ AI Knowledge │    │ Model        │   │
│     └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Файлы для создания

1. **pyrl_oop_plugin.py** - Плагин с OOP функциональностью
2. **pyrl_vm_extended.py** - Расширенная VM с поддержкой классов
3. **oop_examples.pyrl** - Примеры использования OOP
4. **test_oop.py** - Тесты для OOP функциональности
