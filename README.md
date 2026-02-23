# Pyrl Language

**Pyrl** — гибридный язык программирования, вдохновлённый Python и Perl. Сочетает чистый синтаксис Python с мощной системой сигилов Perl.

## Ключевые особенности

- **Сигилы переменных**: `$scalar`, `@array`, `%hash`, `&function`
- **Python-синтаксис**: отступы вместо фигурных скобок
- **Анонимные функции**: `&name($params) = { body }`
- **ООП**: классы, методы, свойства
- **Динамическая типизация**: типы проверяются во время выполнения
- **Богатая стандартная библиотека**: математика, строки, списки, хеши
- **HTTP/JSON**: встроенная поддержка веб-запросов
- **Lark-парсер**: грамматика на основе EBNF

## Установка

```bash
# Клонирование репозитория
git clone http://178.140.10.58:8082/ai/pyrl-project.git
cd pyrl-project

# Установка зависимостей
pip install -r requirements.txt
```

## Быстрый старт

### Hello World

```pyrl
print("Hello, World!")
```

### Переменные

```pyrl
$name = "Alice"
$age = 30
@scores = [95, 87, 92, 88]
%person = {name: "Bob", age: 25}
```

### Функции

```pyrl
# Традиционный синтаксис
def greet($name):
    print("Привет, " + $name + "!")

greet("Мир")

# Анонимные функции
&double($x) = {
    return $x * 2
}

print(&double(5))  # 10

# Ссылка на функцию
$func = &double
print($func(7))  # 14
```

### Анонимные функции с блоками

```pyrl
&reverse_string($str) = {
    $reversed = "";
    $len = len($str);
    $i = $len - 1;
    while $i >= 0 {
        $reversed = $reversed + $str[$i];
        $i = $i - 1
    };
    return $reversed
}

print(&reverse_string("hello"))  # "olleh"

# Проверка палиндрома
&is_palindrome($str) = {
    $clean = lower($str);
    $rev = &reverse_string($clean);
    return $clean == $rev
}

print(&is_palindrome("racecar"))  # True
print(&is_palindrome("hello"))    # False
```

### ООП - Классы

```pyrl
class Person {
    prop name = "Unknown"
    prop age = 0
    
    init($name, $age) = {
        $name = $name;
        $age = $age
    }
    
    method get_name() = {
        return $name
    }
    
    method greet() = {
        return "Привет, я " + $name
    }
}

# Создание экземпляра
$p = Person("Alice", 30)
print($p.get_name())  # "Alice"
print($p.greet())     # "Привет, я Alice"
```

### Циклы

```pyrl
for $i in range(5):
    print($i)

# Цикл внутри блока
&print_numbers($n) = {
    $i = 0;
    while $i < $n {
        print($i);
        $i = $i + 1
    }
}

&print_numbers(5)
```

## Синтаксис

### Сигилы

| Сигил | Тип | Пример |
|-------|-----|--------|
| `$` | Скаляр | `$name = "Alice"` |
| `@` | Массив | `@items = [1, 2, 3]` |
| `%` | Хеш | `%person = {name: "Bob"}` |
| `&` | Функция | `&func = &greet` |

### Доступ к элементам

```pyrl
# Массивы - квадратные скобки
$first = @numbers[0]

# Хеши - квадратные скобки (Python-style)
$name = %person["name"]
```

### Управляющие конструкции

```pyrl
if $x > 0:
    print("Положительное")
elif $x < 0:
    print("Отрицательное")
else:
    print("Ноль")
```

### Блочный синтаксис

```pyrl
# Условия внутри блоков
&abs($x) = {
    if $x < 0 {
        return -$x
    };
    return $x
}

# Циклы внутри блоков
&sum_to($n) = {
    $sum = 0;
    for $i in range($n + 1) {
        $sum = $sum + $i
    };
    return $sum
}
```

## CLI

```bash
# Запуск файла
python pyrl_cli.py examples/01_hello_world.pyrl

# Интерактивный REPL
python pyrl_cli.py

# Выполнение кода из строки
python pyrl_cli.py -c '$x = 10; print($x)'

# Показать AST
python pyrl_cli.py -p script.pyrl

# Режим отладки
python pyrl_cli.py -d script.pyrl

# Запуск веб-сервера
python scripts/run_web_app.py

# Запуск примеров
python scripts/run_examples.py

# Генерация примеров
python scripts/generate_examples.py

# Обучение модели
python scripts/train_model.py
```

## API Server

```bash
# Запуск сервера
python scripts/pyrl_server.py

# Или через uvicorn
uvicorn scripts.pyrl_server:app --host 0.0.0.0 --port 8000

# Выполнение кода
curl -X POST http://localhost:8000/execute \
    -H "Content-Type: application/json" \
    -d '{"code": "$x = 10\nprint($x)"}'
```

## Примеры

### Факториал

```pyrl
def factorial($n):
    if $n <= 1:
        return 1
    return $n * factorial($n - 1)

print(factorial(5))  # 120
```

### Числа Фибоначчи

```pyrl
def fibonacci($n):
    if $n <= 1:
        return $n
    return fibonacci($n - 1) + fibonacci($n - 2)

for $i in range(10):
    print(fibonacci($i))
```

### Фильтрация списка

```pyrl
&filter_positive(@numbers) = {
    @result = [];
    for $n in @numbers {
        if $n > 0 {
            append(@result, $n)
        }
    };
    return @result
}

@nums = [-2, 5, -1, 8, 0, 3]
@positive = &filter_positive(@nums)
print(@positive)  # [5, 8, 3]
```

## Структура проекта

```
pyrl/
├── pyrl_cli.py           # CLI интерфейс
├── src/
│   ├── config.py         # Централизованная конфигурация
│   └── core/
│       ├── lark_parser.py    # Lark-парсер с грамматикой
│       ├── exceptions.py     # Исключения
│       └── vm/               # Виртуальная машина
│           ├── vm.py             # Главная VM
│           ├── environment.py    # Управление областями видимости
│           ├── objects.py        # OOP объекты
│           ├── builtins.py       # Встроенные функции
│           ├── builtins_http.py  # HTTP функции
│           ├── builtins_db.py    # SQLite функции
│           └── builtins_crypto.py # Криптография
├── scripts/              # Скрипты утилиты
│   ├── generate_examples.py  # Генератор примеров
│   ├── generate_model.py     # Генератор модели
│   ├── run_examples.py       # Запуск примеров
│   ├── run_web_app.py        # Веб-сервер
│   └── train_model.py        # Обучение модели
├── examples/             # Примеры кода
├── tests/                # Тесты pytest (321 тест)
├── models/               # ML модель
├── data/                 # Runtime данные
├── cache/                # Кэш и чекпоинты
├── docker/               # Docker конфигурации
└── documents/            # Документация
```

## Запуск тестов

```bash
# Все тесты
pytest tests/ -v

# С покрытием кода
pytest tests/ --cov=src --cov-report=term-missing
```

## Новое в версии 2.0.0

- **Анонимные функции**: `&name($params) = { body }`
- **ООП**: классы с методами и свойствами
- **Блочный синтаксис**: `{ stmt; stmt }`
- **Исправлено затенение переменных**: переменные не затеняют встроенные функции

## Лицензия

MIT License

---

**Pyrl Team**  
Репозиторий: http://178.140.10.58:8082/ai/pyrl-project.git
