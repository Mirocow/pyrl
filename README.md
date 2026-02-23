# Pyrl Language

**Pyrl** — это гибридный язык программирования, вдохновлённый Python и Perl. Он сочетает чистый синтаксис Python с мощной системой сигилов Perl.

## Ключевые особенности

- **Сигилы переменных**: `$scalar`, `@array`, `%hash`, `&function`
- **Python-синтаксис**: отступы вместо фигурных скобок
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
def greet($name):
    print("Привет, " + $name + "!")

greet("Мир")
```

### Циклы

```pyrl
for $i in range(5):
    print($i)
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

### Циклы

```pyrl
# For loop
for $item in @items:
    print($item)

# While loop
while $x < 10:
    $x = $x + 1
```

## CLI

```bash
# Запуск файла
python pyrl_cli.py examples/01_hello_world.pyrl

# Интерактивный REPL
python pyrl_cli.py

# Запуск сервера
python pyrl_server.py
```

## API Server

```bash
# Запуск сервера
uvicorn pyrl_server:app --host 0.0.0.0 --port 8000

# Выполнение кода
curl -X POST http://localhost:8000/execute \
    -H "Content-Type: application/json" \
    -d '{"code": "$x = 10\nprint($x)"}'
```

## Структура проекта

```
pyrl/
├── src/core/
│   ├── lark_parser.py    # Lark-парсер с грамматикой
│   ├── vm.py             # Виртуальная машина
│   ├── builtins.py       # Встроенные функции
│   ├── lexer.py          # Лексер (legacy)
│   └── parser.py         # Парсер (legacy)
├── examples/             # Примеры кода
├── tests/                # Тесты pytest
├── models/               # ML модель
├── docker/               # Docker конфигурации
└── documents/            # Документация
```

## Запуск тестов

```bash
pytest tests/ -v
```

## Лицензия

MIT License

---

**Pyrl Team**  
Репозиторий: http://178.140.10.58:8082/ai/pyrl-project.git
