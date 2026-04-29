---
tags: [nexus-vault, enterprise, design-system, accessibility, ui, vmware]
category: Web / UI Design Frameworks (Enterprise)
language: HTML / CSS / Angular / React / Vue
github: https://github.com/vmware-archive/clarity
---

# CLARITY — Enterprise Design System (VMware)

## Описание
**Clarity** — это серьезная **Enterprise-дизайн-система** от **VMware**. Она объединяет UX-принципы, набор HTML/CSS фреймворков и библиотеку Angular-компонентов. В отличие от "модных" Chakra или Tailwind, Clarity сфокусирована на **сложных данных**, управлении облаками, виртуализацией и огромными дашбордами с тысячами элементов.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Core | HTML / Modern CSS (Custom Properties) |
| Framework | Angular (Native) / React & Vue (via Core) |
| Icons | Clarity Icons (Icon collection) |
| Layout | Clarity Grids & Layout systems |
| Accessibility | W3C / WCAG compliant (AA standard) |

## Кому это нужно (Особенности)
1. **Data Density**— Идеально для приложений с высокой плотностью данных (таблицы, списки ресурсов).
2. **Datagrid**— Одна из лучших реализаций таблиц: фильтрация, сортировка, пагинация, "липкие" колонки — всё из коробки.
3. **Enterprise UI Components**— Стейпперы, модальные окна, визарды (Step-by-step wizards) для настройки серверов.
4. **Visual Language**— Строгий, профессиональный вид, вызывающий доверие у корпоративных клиентов.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Информационная Емкость (Information Density). Идеально для основного интерфейса **NEXUS Orchestrator Control Panel**.
- **Интеграция:** Использование Clarity Datagrid для управления списком из 1400+ репозиториев (поиск, тегирование, массовая обработка).
- **Ключевое:** Поддержка сложной навигации (Side Navigation + Subnav).

## Пример разметки (HTML)
```html
<clr-main-container>
  <clr-header class="header-6">
    <div class="branding">NEXUS ENTERPRISE</div>
  </clr-header>
  <div class="content-container">
    <nav class="sidenav"></nav>
    <main class="content-area">
      <!-- Место для вашего Дашборда -->
    </main>
  </div>
</clr-main-container>
```

## Связанные Репозитории
- [[CHAKRA-UI]] — более "легкий" дизайн
- [[ANT-DESIGN]] — конкурент в энтерпрайзе
- [[BUN]] / [[NODE-JS]] — где этот фронтенд работает
- [[ASTRO]] — современная сборка
- [[ANYTHING-LLM]] — клиентский интерфейс
