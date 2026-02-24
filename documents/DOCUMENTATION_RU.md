# Документация языка Pyrl

**Версия:** 2.1.0  
**Последнее обновление:** 2025-02-24

---

## Оглавление

1. [Введение](#введение)
2. [Установка](#установка)
3. [Быстрый старт](#быстрый-старт)
4. [Синтаксис](#синтаксис)
5. [Переменные и сигилы](#переменные-и-сигилы)
6. [Типы данных](#типы-данных)
7. [Операторы](#операторы)
8. [Управляющие конструкции](#управляющие-конструкции)
9. [Функции](#функции)
10. [Анонимные функции](#анонимные-функции) *(NEW v2.0)*
11. [Классы и объекты](#классы-и-объекты) *(NEW v2.0)*
12. [Встроенные функции](#встроенные-функции)
13. [API сервер](#api-сервер)
14. [Docker](#docker)
15. [Примеры](#примеры)

---

## Введение

Pyrl — это гибридный язык программирования, вдохновлённый Python и Perl. Он сочетает чистый синтаксис Python с мощной системой сигилов Perl, предоставляя уникальный опыт программирования.

### Ключевые особенности

- **Сигилы переменных**: `$scalar`, `@array`, `%hash`, `&function`
- **Python-синтаксис**: отступы вместо фигурных скобок
- **Динамическая типизация**: типы проверяются во время выполнения
- **Богатая стандартная библиотека**: математика, строки, списки, хеши
- **Система плагинов**: расширяемая архитектура
- **HTTP/JSON**: встроенная поддержка веб-запросов
- **Обучение модели**: возможность обучить модель на примерах Pyrl

---

## Установка

### Из исходного кода

```bash
# Клонирование репозитория
git clone http://178.140.10.58:8082/ai/pyrl-project.git
cd pyrl-project

# Установка зависимостей
pip install -r requirements.txt

# Установка в режиме разработки
pip install -e .
```

### Через Docker

```bash
# Сборка образа
docker build -f docker/Dockerfile.server -t pyrl-server:latest .

# Запуск контейнера
docker run -p 8000:8000 pyrl-server:latest
```

### Проверка установки

```bash
# Запуск REPL
python pyrl_cli.py

# Проверка версии
python pyrl_cli.py --version
```

---

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

---

## Синтаксис

### Структура программы

Программы на Pyrl состоят из последовательности операторов. Блоки кода выделяются отступами (как в Python), а не фигурными скобками.

```pyrl
# Комментарий
$x = 10

if $x > 0:
    # Блок с отступом
    print("Положительное")
elif $x < 0:
    print("Отрицательное")
else:
    print("Ноль")
```

### Отступы

Используйте 4 пробела для отступов (рекомендуется) или табуляцию. Смешивание не допускается.

```pyrl
# Правильно
if True:
    print("OK")
    if False:
        print("Nested")

# Неправильно (смешанные отступы)
if True:
        print("Tab")
    print("Spaces")  # Ошибка!
```

---

## Переменные и сигилы

### Сигилы

Pyrl использует сигилы для обозначения типа переменной:

| Сигил | Тип | Описание |
|-------|-----|----------|
| `$` | Скаляр | Одно значение (число, строка, булево) |
| `@` | Массив | Упорядоченный список значений |
| `%` | Хеш | Словарь ключ-значение |
| `&` | Функция | Ссылка на функцию |

### Скаляры

```pyrl
$name = "Alice"
$age = 30
$pi = 3.14159
$active = True
```

### Массивы

```pyrl
@numbers = [1, 2, 3, 4, 5]
@mixed = [1, "two", 3.0, True]
@empty = []

# Доступ по индексу
$first = @numbers[0]
$last = @numbers[-1]

# Срезы
@subset = @numbers[1:3]
```

### Хеши

```pyrl
%person = {name: "Alice", age: 30, active: True}

# Доступ по ключу (Python-style квадратные скобки)
$name = %person["name"]
$age = %person["age"]

# Добавление/изменение
%person["email"] = "alice@example.com"
```

### Функциональные ссылки

```pyrl
def double($x):
    return $x * 2

&func = &double
$result = &func(5)  # 10
```

---

## Типы данных

### Числа

```pyrl
$int = 42
$float = 3.14159
$neg = -17
$hex = 0xFF
$bin = 0b1010
$sci = 1.5e10
```

### Строки

```pyrl
$single = 'Hello'
$double = "World"
$multi = """
Многострочная
строка
"""

# Интерполяция (в двойных кавычках)
$name = "Alice"
$greeting = "Привет, $name!"
```

### Логические значения

```pyrl
$true = True
$false = False
```

### None

```pyrl
$value = None
```

---

## Операторы

### Арифметические

| Оператор | Описание | Пример |
|----------|----------|--------|
| `+` | Сложение | `5 + 3` → `8` |
| `-` | Вычитание | `5 - 3` → `2` |
| `*` | Умножение | `5 * 3` → `15` |
| `/` | Деление | `6 / 3` → `2.0` |
| `//` | Целочисленное деление | `7 // 3` → `2` |
| `%` | Остаток от деления | `7 % 3` → `1` |
| `**` | Возведение в степень | `2 ** 3` → `8` |

### Сравнения

| Оператор | Описание | Пример |
|----------|----------|--------|
| `==` | Равно | `5 == 5` → `True` |
| `!=` | Не равно | `5 != 3` → `True` |
| `<` | Меньше | `3 < 5` → `True` |
| `>` | Больше | `5 > 3` → `True` |
| `<=` | Меньше или равно | `3 <= 3` → `True` |
| `>=` | Больше или равно | `5 >= 3` → `True` |

### Логические

| Оператор | Описание | Пример |
|----------|----------|--------|
| `and` | Логическое И | `True and False` → `False` |
| `or` | Логическое ИЛИ | `True or False` → `True` |
| `not` | Логическое НЕ | `not True` → `False` |

---

## Управляющие конструкции

### Условия (if/elif/else)

```pyrl
$x = 10

if $x > 0:
    print("Положительное")
elif $x < 0:
    print("Отрицательное")
else:
    print("Ноль")
```

### Цикл for

```pyrl
# Итерация по диапазону
for $i in range(5):
    print($i)

# Итерация по массиву
@items = ["яблоко", "банан", "апельсин"]
for $item in @items:
    print($item)

# Итерация с индексом
for $i, $item in enumerate(@items):
    print($i + ": " + $item)
```

### Цикл while

```pyrl
$x = 0
while $x < 10:
    print($x)
    $x = $x + 1
```

### break и continue

```pyrl
for $i in range(10):
    if $i == 3:
        continue  # Пропустить 3
    if $i == 7:
        break     # Остановить на 7
    print($i)
```

---

## Функции

### Определение функции

```pyrl
def greet($name):
    print("Привет, " + $name + "!")

greet("Alice")
```

### Возврат значения

```pyrl
def add($a, $b):
    return $a + $b

$result = add(5, 3)  # 8
```

### Функциональные ссылки

```pyrl
def double($x):
    return $x * 2

&func = &double
$result = &func(5)  # 10
```

---

## Анонимные функции *(NEW v2.0)*

### Основной синтаксис

Анонимные функции определяются с помощью блочного синтаксиса:

```pyrl
&double($x) = {
    return $x * 2
}

print(&double(5))  # 10
```

### Блочный синтаксис

Тело функции заключается в фигурные скобки, операторы разделяются точкой с запятой:

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
```

### Управляющие конструкции в блоках

Внутри блоков можно использовать `if`, `while`, `for`:

```pyrl
&abs($x) = {
    if $x < 0 {
        return -$x
    };
    return $x
}

&sum_to($n) = {
    $sum = 0;
    for $i in range($n + 1) {
        $sum = $sum + $i
    };
    return $sum
}

print(&abs(-5))      # 5
print(&sum_to(10))   # 55
```

### Ссылки на функции

Функции можно сохранять в переменные и передавать:

```pyrl
&greet($name) = {
    return "Hello, " + $name + "!"
}

$greeter = &greet
print($greeter("World"))  # "Hello, World!"
```

### Вложенные вызовы

Функции могут вызывать другие функции:

```pyrl
&is_palindrome($str) = {
    $clean = lower($str);
    $rev = &reverse_string($clean);
    return $clean == $rev
}

print(&is_palindrome("racecar"))  # True
print(&is_palindrome("hello"))    # False
```

---

## Классы и объекты *(NEW v2.0)*

### Определение класса

Pyrl поддерживает ООП с синтаксисом классов:

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
```

### Создание экземпляра

```pyrl
$p = Person("Alice", 30)
print($p.get_name())  # "Alice"
print($p.greet())     # "Привет, я Alice"
```

### Свойства (prop)

Свойства определяются с ключевым словом `prop`:

```pyrl
class Rectangle {
    prop width = 0
    prop height = 0
    prop area = 0
    
    init($w, $h) = {
        $width = $w;
        $height = $h;
        $area = $width * $height
    }
}

$rect = Rectangle(5, 3)
print($rect.area)  # 15
```

### Методы (method)

Методы определяются с ключевым словом `method`:

```pyrl
class Counter {
    prop count = 0
    
    method increment() = {
        $count = $count + 1
    }
    
    method get() = {
        return $count
    }
}

$c = Counter()
$c.increment()
$c.increment()
print($c.get())  # 2
```

### Конструктор (init)

Конструктор определяется с ключевым словом `init`:

```pyrl
class Point {
    prop x = 0
    prop y = 0
    
    init($x, $y) = {
        $x = $x;
        $y = $y
    }
    
    method distance() = {
        return sqrt($x * $x + $y * $y)
    }
}

$p = Point(3, 4)
print($p.distance())  # 5.0
```

### Пример: Стек

```pyrl
class Stack {
    prop items = []
    
    init() = {
        $items = []
    }
    
    method push($item) = {
        append($items, $item)
    }
    
    method pop() = {
        return pop($items)
    }
    
    method is_empty() = {
        return len($items) == 0
    }
}

$stack = Stack()
$stack.push(1)
$stack.push(2)
$stack.push(3)
print($stack.pop())       # 3
print($stack.is_empty())  # False
```

---

## Встроенные функции

### Ввод/вывод

| Функция | Описание |
|---------|----------|
| `print(*args)` | Вывод в консоль |
| `input(prompt)` | Чтение из консоли |

### Типы

| Функция | Описание |
|---------|----------|
| `int(x)` | Преобразование в целое |
| `float(x)` | Преобразование в дробное |
| `str(x)` | Преобразование в строку |
| `bool(x)` | Преобразование в булево |
| `list(x)` | Преобразование в список |
| `dict(x)` | Преобразование в словарь |
| `type(x)` | Тип значения |

### Математика

| Функция | Описание |
|---------|----------|
| `abs(x)` | Модуль числа |
| `round(x, n)` | Округление |
| `min(*args)` | Минимум |
| `max(*args)` | Максимум |
| `sum(iter)` | Сумма |
| `pow(x, y)` | Степень |
| `sqrt(x)` | Квадратный корень |
| `sin(x)`, `cos(x)`, `tan(x)` | Тригонометрия |
| `log(x, base)` | Логарифм |
| `exp(x)` | Экспонента |
| `floor(x)`, `ceil(x)` | Округление вниз/вверх |

### Строки

| Функция | Описание |
|---------|----------|
| `lower(s)` | В нижний регистр |
| `upper(s)` | В верхний регистр |
| `strip(s)` | Удалить пробелы |
| `split(s, sep)` | Разбить строку |
| `join(sep, list)` | Объединить строки |
| `replace(s, old, new)` | Замена |
| `find(s, sub)` | Поиск подстроки |
| `startswith(s, prefix)` | Начинается с |
| `endswith(s, suffix)` | Заканчивается на |

### Списки

| Функция | Описание |
|---------|----------|
| `append(list, x)` | Добавить элемент |
| `extend(list, items)` | Расширить список |
| `insert(list, i, x)` | Вставить элемент |
| `remove(list, x)` | Удалить элемент |
| `pop(list, i)` | Извлечь элемент |
| `sort(list)` | Сортировка |
| `reverse(list)` | Разворот |
| `len(list)` | Длина |

### Хеши

| Функция | Описание |
|---------|----------|
| `keys(dict)` | Ключи |
| `values(dict)` | Значения |
| `items(dict)` | Пары ключ-значение |
| `get(dict, key, default)` | Получить значение |

### Регулярные выражения

| Функция | Описание |
|---------|----------|
| `re_match(pattern, string)` | Поиск в начале |
| `re_search(pattern, string)` | Поиск в строке |
| `re_findall(pattern, string)` | Все совпадения |
| `re_sub(pattern, repl, string)` | Замена по шаблону |

### HTTP и JSON

| Функция | Описание |
|---------|----------|
| `http_get(url, timeout)` | HTTP GET запрос |
| `http_post(url, data, timeout)` | HTTP POST запрос |
| `json_parse(string)` | Парсинг JSON |
| `json_stringify(obj, indent)` | Сериализация в JSON |

---

## Система плагинов

### Загрузка встроенных плагинов

```pyrl
# Функция load_builtin_plugins() загружает все встроенные функции
# и возвращает их в виде словаря
$plugins = load_builtin_plugins()
$plugins{"print"}("Hello!")
```

### Регистрация пользовательского плагина

```python
# В Python коде
from src.core.builtins import register_plugin

def my_function(x):
    return x * 2

register_plugin("myplugin", {"double": my_function})
```

### Использование в Pyrl

```pyrl
$result = myplugin_double(5)  # 10
```

### Переменная окружения PYRL_PLUGINS_PATH

```bash
export PYRL_PLUGINS_PATH=/path/to/plugins:/another/path
python pyrl_cli.py
```

---

## Обучение модели

Pyrl включает систему обучения языковой модели на примерах кода. Модель изучает синтаксис и паттерны языка Pyrl.

### Структура модели

```
models/pyrl-model/
├── config.json           # Конфигурация модели (768 hidden, 12 layers)
├── pytorch_model.bin     # Веса модели
├── vocab.json           # Словарь токенов (1778 токенов)
├── tokenizer_config.json # Конфигурация токенизатора
├── special_tokens_map.json
└── training_stats.json  # Статистика обучения
```

### Обучение через CLI

В интерактивном REPL:

```
pyrl> train                          # Обучить с настройками по умолчанию
pyrl> train --epochs 20 --batch-size 64
pyrl> train --examples path/to/examples.pyrl
```

### Обучение через Makefile

```bash
make train          # Обучить модель (10 epochs)
make train-full     # Полное обучение (20 epochs, batch 64)
make train-quick    # Быстрое обучение (3 epochs)
make train-custom EXAMPLES=path EPOCHS=20
```

### Обучение через скрипт

```bash
# Базовое обучение
python scripts/train_model.py --examples examples/10000_examples.pyrl

# С параметрами
python scripts/train_model.py \
    --examples examples/10000_examples.pyrl \
    --epochs 20 \
    --batch-size 64 \
    --learning-rate 0.0001 \
    --hidden-size 768 \
    --layers 12

# Из директории с примерами
python scripts/train_model.py --examples-dir examples/
```

### Параметры обучения

| Параметр | По умолчанию | Описание |
|----------|--------------|----------|
| `--examples` | - | Путь к файлу с примерами |
| `--examples-dir` | - | Путь к директории с примерами |
| `--output` | models/pyrl-model | Папка для сохранения модели |
| `--epochs` | 10 | Количество эпох обучения |
| `--batch-size` | 32 | Размер батча |
| `--learning-rate` | 0.0001 | Скорость обучения |
| `--max-length` | 512 | Максимальная длина последовательности |
| `--hidden-size` | 768 | Размер скрытого слоя |
| `--layers` | 12 | Количество слоёв трансформера |
| `--heads` | 12 | Количество голов внимания |

### Токенизатор Pyrl

Pyrl использует специализированный токенизатор с поддержкой:

**Специальные токены:**
- `<pad>`, `<unk>`, `<bos>`, `<eos>`, `<mask>`
- `<newline>`, `<indent>`, `<dedent>`

**Сигилы:**
- `$` (скаляр), `@` (массив), `%` (хеш), `&` (функция)

**Ключевые слова:**
- `if`, `elif`, `else`, `while`, `for`, `in`, `def`, `return`, `class`, `lambda` и др.

**Операторы:**
- `+`, `-`, `*`, `/`, `**`, `//`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `=` и др.

**Встроенные функции:**
- `print`, `len`, `range`, `str`, `int`, `float`, `list`, `dict` и др.

### Результаты обучения

| Метрика | Значение |
|---------|----------|
| Примеров | 334 |
| Токенов | 13,898 |
| Словарь | 1,778 |
| Val Loss | 0.70 |

### Чекпоинты

Во время обучения сохраняются чекпоинты:

```
checkpoints/
├── checkpoint_epoch_1.json
├── checkpoint_epoch_2.json
└── ...
```

Каждый чекпоинт содержит:
- Номер эпохи
- Validation loss
- Размер словаря
- Временную метку

---

## API сервер

### Запуск сервера

```bash
# Режим разработки
python pyrl_server.py

# Через uvicorn
uvicorn pyrl_server:app --host 0.0.0.0 --port 8000
```

### Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Информация о сервере |
| GET | `/health` | Проверка здоровья |
| POST | `/execute` | Выполнение кода |
| POST | `/tokenize` | Токенизация |
| POST | `/parse` | Парсинг в AST |
| POST | `/reset` | Сброс VM |
| GET | `/variables` | Получить переменные |
| GET | `/plugins` | Загруженные плагины |
| POST | `/plugins/load` | Загрузить плагин |
| GET | `/config` | Конфигурация |
| GET | `/stats` | Статистика сервера |

### Примеры запросов

**Выполнение кода:**

```bash
curl -X POST http://localhost:8000/execute \
    -H "Content-Type: application/json" \
    -d '{"code": "$x = 10\nprint($x)"}'
```

**Ответ:**

```json
{
    "success": true,
    "result": null,
    "output": "10\n",
    "variables": {"x": 10}
}
```

**Токенизация:**

```bash
curl -X POST http://localhost:8000/tokenize \
    -H "Content-Type: application/json" \
    -d '{"code": "$x = 10"}'
```

---

## Docker

### Доступные образы

| Образ | Описание |
|-------|----------|
| `Dockerfile.server` | API сервер |
| `Dockerfile.console` | CLI консоль |
| `Dockerfile.dev` | Среда разработки |
| `Dockerfile.training` | Обучение модели |
| `Dockerfile.model-generator` | Генерация модели |
| `Dockerfile.model-inference` | Инференс модели |

### Сборка и запуск

```bash
# Сборка всех образов
make docker-build

# Запуск сервера
make docker-run-server

# Запуск через docker-compose
make docker-up
```

### Docker Compose

```yaml
services:
  pyrl-server:
    build:
      context: .
      dockerfile: docker/Dockerfile.server
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
```

---

## Примеры

### Факториал

```pyrl
def factorial($n):
    if $n <= 1:
        return 1
    return $n * factorial($n - 1)

$result = factorial(5)  # 120
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

### Сортировка пузырьком

```pyrl
def bubble_sort(@arr):
    $n = len(@arr)
    for $i in range($n):
        for $j in range($n - $i - 1):
            if @arr[$j] > @arr[$j + 1]:
                $temp = @arr[$j]
                @arr[$j] = @arr[$j + 1]
                @arr[$j + 1] = $temp
    return @arr

@sorted = bubble_sort([64, 34, 25, 12, 22, 11, 90])
```

### HTTP запрос

```pyrl
$response = http_get("https://api.example.com/data")
if $response{"status"} == 200:
    $data = json_parse($response{"data"})
    print($data)
```

---

## Веб-сервер с авторизацией *(NEW v2.1)*

Полный пример веб-приложения на Pyrl с фронтендом и бэкендом находится в `examples/web_server_auth.pyrl`.

### Запуск сервера

```bash
cd pyrl-project
python scripts/run_web_app.py --file examples/web_server_auth.pyrl --port 8080
```

После запуска сервер доступен по адресу: `http://localhost:8080/`

### Структура pyrl-файла

```pyrl
# 1. КОНФИГУРАЦИЯ
$APP_NAME = "Pyrl Admin"
$APP_VERSION = "1.0.0"
$PORT = env_get("PYRL_PORT", "8080")
$SECRET_KEY = env_get("PYRL_SECRET", "pyrl_secret_key_2024")

# 2. ДАННЫЕ (база пользователей в памяти)
%users = {
    "admin": {password: "admin123", role: "Administrator", name: "Admin User"},
    "user": {password: "user123", role: "User", name: "John Doe"}
}

%sessions = {}

# 3. БИЗНЕС-ЛОГИКА
def check_login($username, $password):
    $user = get(%users, $username, None)
    if $user != None:
        if $user["password"] == $password:
            return $user
    return None

def create_session($username):
    $token = generate_token($username)
    %sessions[$token] = {username: $username, expires: time() + 3600}
    return $token

# 4. HTTP ОБРАБОТЧИК (точка входа)
def handle_request($method, $path, %headers, $body):
    if $path == "/" and $method == "GET":
        return html_response($LOGIN_PAGE)
    
    if $path == "/login" and $method == "POST":
        %form = parse_form($body)
        $user = check_login(%form["username"], %form["password"])
        if $user == None:
            return {status: 302, headers: {"Location": "/?error=1"}, body: ""}
        $token = create_session(%form["username"])
        return {status: 302, headers: {"Location": "/dashboard", "Set-Cookie": "session=" + $token}, body: ""}
    
    # ... другие маршруты
    
    return html_response($ERROR_PAGE, 404)

# 5. ЭКСПОРТ (обязательно!)
$app = {handle: &handle_request, port: int($PORT)}
```

### Web-интерфейс

| URL | Описание |
|-----|----------|
| `GET /` | Страница входа с красивым UI |
| `POST /login` | Обработка авторизации |
| `GET /dashboard` | Дашборд после авторизации |
| `POST /logout` | Выход из системы |

### REST API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/status` | Статус сервера |
| GET | `/api/users` | Список пользователей |
| GET | `/api/user/{name}` | Информация о пользователе |
| POST | `/api/verify` | Проверка credentials (JSON) |
| POST | `/api/validate` | Проверка токена сессии |
| POST | `/api/logout` | Выход (API) |

### Примеры API-запросов

```bash
# Проверка credentials
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}' \
     http://localhost:8080/api/verify

# Ответ: {"success": true, "token": "...", "user": {...}}

# Статус сервера
curl http://localhost:8080/api/status

# Список пользователей
curl http://localhost:8080/api/users
```

### Тестовые учётные данные

| Логин | Пароль | Роль |
|-------|--------|------|
| `admin` | `admin123` | Administrator |
| `user` | `user123` | User |
| `guest` | `guest123` | Guest |

### Поток авторизации

```
1. GET /               → Отображение формы входа
2. POST /login         → Проверка credentials
   ├─ Success          → Создание сессии, redirect /dashboard
   └─ Failed           → Redirect /?error=1
3. GET /dashboard      → Проверка сессии через cookie
   ├─ Valid session    → Отображение дашборда
   └─ Invalid/None     → Redirect /
4. POST /logout        → Удаление cookie, redirect /
```

### Пример приложения без авторизации

Файл `examples/app.pyrl` — простой шаблон приложения с бизнес-логикой:

```pyrl
# Данные
@items = [
    {id: 1, name: "Item One", value: 100},
    {id: 2, name: "Item Two", value: 200}
]

# Бизнес-логика
def get_all_items():
    return @items

def add_item($name, $value):
    $new_id = len(@items) + 1
    append(@items, {id: $new_id, name: $name, value: $value})

# HTTP обработчик
def handle_request($method, $path, %headers, $body):
    if $path == "/api/items" and $method == "GET":
        return json_response({items: get_all_items()})
    if $path == "/api/items" and $method == "POST":
        %data = json_parse($body)
        add_item(%data["name"], %data["value"])
        return json_response({success: True})
    return json_response({error: "Not found"}, 404)

$app = {handle: &handle_request}
```

---

## Константы

| Константа | Значение | Описание |
|-----------|----------|----------|
| `True` | `True` | Истина |
| `False` | `False` | Ложь |
| `None` | `None` | Пустое значение |
| `PI` | 3.141592653589793 | Число π |
| `E` | 2.718281828459045 | Число e |
| `INF` | `float('inf')` | Бесконечность |
| `NAN` | `float('nan')` | Не число |

---

## Лицензия

MIT License

---

**Pyrl Team**  
Репозиторий: http://178.140.10.58:8082/ai/pyrl-project.git
