---
tags: [nexus-vault, software-quality, clean-code, javascript, best-practices]
category: Education / Software Engineering (Clean Code)
language: JavaScript / Node.js
github: https://github.com/ryanmcdermott/clean-code-javascript
---

# CLEAN-CODE-JAVASCRIPT — Software Engineering Best Practices

## Описание
**Clean Code JavaScript** — это адаптация принципов из легендарной книги Роберта Мартина "Чистый код" для языка **JavaScript**. Это набор правил и руководств, которые позволяют писать код, который **легко читать, легко тестировать и легко поддерживать**. Это стандарт, по которому работают лучшие инженерные команды мира.

## Ключевые Принципы (Выжимка)
1. **Meaningful Names**— "Зачем ты здесь?". Имена переменных должны отвечать на вопрос о их назначении: `daysSinceCreation` вместо `d`.
2. **Small Functions**— Функции должны делать **одну вещь**, иметь минимум аргументов и быть короткими (до 20-30 строк).
3. **Don't use Flags**— Использование булевых "флагов" внутри функций говорит о том, что функция делает больше одной вещи.
4. **DRY (Don't Repeat Yourself)**— Любое дублирование кода — это баг будущего. Выноси общую логику в абстракции.
5. **ES6 Essentials**— Используй классы, стрелочные функции, деструктуризацию, чтобы код был лаконичным.
6. **Error Handling**— Никогда не игнорируй ошибки и не оставляй пустых блоков `catch`.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Качество Автоматического Кода (Code Quality Assurance). Агенты-Конструкторы NEXUS должны писать код именно по этим правилам.
- **Интеграция:** Модуль NEXUS Code Auditor — автоматическая проверка кода новых репозиториев на соответствие правилам "чистоты".
- **Ключевое:** Читаемость кода важнее его написания (код читается в 10 раз чаще, чем пишется).

## Пример: Плохо vs Хорошо
```javascript
// ПЛОХО: Непонятное имя, магическое число
const d = 86400; 

// ХОРОШО: Имя объясняет суть
const SECONDS_IN_A_DAY = 86400;

// ПЛОХО: Функция делает всё
function emailUsers(users) {
  users.forEach(u => {
    if (u.isActive) sendEmail(u);
  });
}

// ХОРОШО: Разделение ответственности
function getActiveUsers(users) {
  return users.filter(u => u.isActive);
}
function emailUsers(users) {
  getActiveUsers(users).forEach(sendEmail);
}
```

## Связанные Репозитории
- [[APPLICATIONINSPECTOR]] — как Microsoft анализирует код
- [[ALGS4]] — классика "чистого" алгоритмического кода
- [[BUN]] / [[NODE-JS]] — где этот код работает
- [[CHAKRA-UI]] — чистый код в дизайне
- [[GIT-GUIDE]] — как "чисто" сохранять код
- [[BUILD-YOUR-OWN-X]] — создание систем через чистый код
