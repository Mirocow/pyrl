## Задачи для Pyrl Authentication System

### Создание нового компонента Vue

**Последнее выполнение:** 2025-05-25
**Файлы для модификации:**
- `auth_app.pyrl` - Добавить определение компонента Vue

**Шаги:**
1. Определить новый компонент Vue с помощью ключевого слова `vue`
2. Указать название компонента
3. Добавить свойства (props) для компонента
4. Протестировать компонент с помощью существующей системы тестирования

**Пример реализации:**
```pyrl
vue "UserProfile" { 
  title: "User Profile", 
  name_label: "Name", 
  email_label: "Email", 
  save_text: "Save Changes" 
}
```

### Добавление новой функции аутентификации

**Последнее выполнение:** 2025-05-25
**Файлы для модификации:**
- `auth_app.pyrl` - Добавить новую функцию
- При необходимости обновить `pyrl_vm.py` для поддержки новых возможностей

**Шаги:**
1. Определить новую функцию с помощью синтаксиса `&function_name(...) = { ... }`
2. Реализовать логику функции
3. Добавить тесты для новой функции
4. Обновить документацию при необходимости

**Пример реализации:**
```pyrl
&change_password($username, $old_password, $new_password) = {
    if &check_credentials($username, $old_password) == true {
        $user = %users[$username]
        %users[$username] = {"password": &hash_password($new_password), "role": $user["role"], "email": $user["email"]}
        return "Password changed successfully"
    } else { 
        return "Authentication failed" 
    }
}