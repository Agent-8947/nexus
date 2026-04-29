[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40vibecoding_tg%2F%25D0%25BA%25D1%258D%25D1%2588%25D0%25B8%25D1%2580%25D0%25BE%25D0%25B2%25D0%25B0%25D0%25BD%25D0%25B8%25D0%25B5-%25D0%25BF%25D1%2580%25D0%25BE%25D0%25BC%25D0%25BF%25D1%2582%25D0%25BE%25D0%25B2-%25D0%25B2-%25D0%25B1%25D0%25BE%25D0%25BB%25D1%258C%25D1%2588%25D0%25B8%25D1%2585-%25D1%258F%25D0%25B7%25D1%258B%25D0%25BA%25D0%25BE%25D0%25B2%25D1%258B%25D1%2585-%25D0%25BC%25D0%25BE%25D0%25B4%25D0%25B5%25D0%25BB%25D1%258F%25D1%2585-4b47b76b8f10&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40vibecoding_tg%2F%25D0%25BA%25D1%258D%25D1%2588%25D0%25B8%25D1%2580%25D0%25BE%25D0%25B2%25D0%25B0%25D0%25BD%25D0%25B8%25D0%25B5-%25D0%25BF%25D1%2580%25D0%25BE%25D0%25BC%25D0%25BF%25D1%2582%25D0%25BE%25D0%25B2-%25D0%25B2-%25D0%25B1%25D0%25BE%25D0%25BB%25D1%258C%25D1%2588%25D0%25B8%25D1%2585-%25D1%258F%25D0%25B7%25D1%258B%25D0%25BA%25D0%25BE%25D0%25B2%25D1%258B%25D1%2585-%25D0%25BC%25D0%25BE%25D0%25B4%25D0%25B5%25D0%25BB%25D1%258F%25D1%2585-4b47b76b8f10&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# Кэширование промптов в больших языковых моделях

[![@vibecoding_tg](https://miro.medium.com/v2/resize:fill:32:32/1*xw7X9UeF6LOT9hAIKjQiZA.jpeg)](https://medium.com/@vibecoding_tg?source=post_page---byline--4b47b76b8f10---------------------------------------)

[@vibecoding\_tg](https://medium.com/@vibecoding_tg?source=post_page---byline--4b47b76b8f10---------------------------------------)

Follow

6 min read

·

2 hours ago

2

Share

Кейс о том, как Claude достигает 92% cache hit-rate

Каждый раз, когда ИИ-агент делает шаг, он отправляет всю историю диалога обратно в модель.

Туда входят системные инструкции, определения инструментов и контекст проекта, который уже обрабатывался три хода назад. Всё это заново читается, заново обрабатывается и заново тарифицируется на каждом шаге.

![](https://miro.medium.com/v2/resize:fit:680/0*Dx3hHnqy3QShkQ8f)

В долгоживущих агентных воркфлоу такие избыточные вычисления часто становятся самой дорогой строкой затрат во всей ИИ-инфраструктуре.

Системный промпт на 20 000 токенов при 50 шагах — это 1 миллион токенов избыточных вычислений, оплаченных по полной цене и не создающих новой ценности. И эта стоимость накапливается для каждого пользователя и каждой сессии.

Решение — кэширование промптов. Но чтобы использовать его эффективно, нужно понимать, что именно происходит под капотом.

## Статический и динамический контекст

Перед оптимизацией промпта нужно понимать, что меняется, а что остаётся неизменным.

Каждый запрос агента состоит из двух принципиально разных частей:

![](https://miro.medium.com/v2/resize:fit:680/0*0unydVfDCko_cp96)

\- Статический префикс, который не меняется между шагами: системные инструкции, определения инструментов, контекст проекта и поведенческие гайдлайны.

-Динамический суффикс, который растёт на каждом шаге: сообщения пользователя, ответы ассистента, выводы инструментов и наблюдения из терминала.

Именно это разделение делает кэширование промптов возможным. Инфраструктура сохраняет математическое состояние статического префикса, чтобы последующие запросы с тем же префиксом могли полностью пропустить вычисления и читать результат из памяти.

После этого все архитектурные решения, описанные далее, становятся очевидными.

## Как работает KV-кэш

Чтобы понять, почему кэширование даёт такой эффект, нужно разобраться, что трансформер делает при обработке промпта.

Каждый инференс-запрос к модели проходит в две фазы:

![](https://miro.medium.com/v2/resize:fit:680/0*y-ZFvA-rdGBcY-em)

1/ Фаза префилла обрабатывает весь входной промпт. Выполняются плотные матричные умножения по всем токенам в контексте, формируя внутреннее представление модели. Эта фаза ограничена вычислениями и дорогая.

2/ Фаза декодинга генерирует токены по одному. Каждый новый токен добавляется в последовательность, и модель предсказывает следующий. Эта фаза ограничена памятью, так как в основном читает уже накопленное состояние, а не выполняет тяжёлые вычисления.

Во время фазы префилла трансформер вычисляет для каждого токена три вектора: Query, Key и Value. Механизм внимания использует их, чтобы определить, как каждый токен связан с остальными. Векторы Key и Value для конкретного токена зависят только от предыдущих токенов и после вычисления больше не меняются.

Без кэширования эти тензоры Key и Value удаляются после каждого запроса, и при следующем запросе пересчитываются с нуля. Для префикса в 20 000 токенов это означает повторное выполнение внимания по всем 20 000 токенам без необходимости.

KV-кэш решает это, сохраняя тензоры на серверах инференса с привязкой к криптографическому хэшу последовательности токенов. Когда приходит новый запрос с тем же префиксом, хэш совпадает, тензоры загружаются из памяти, и вычисления префилла для этих токенов полностью пропускаются.

Это снижает вычислительную сложность с O(n²) на каждый сгенерированный токен до O(n). Для префикса в 20 000 токенов, повторяющегося на протяжении 50 шагов, выигрыш получается существенный.

## Экономика

Структура ценообразования делает это архитектурное решение критически важным.

Чтение из кэша стоит 0.1x от базовой цены входных токенов, то есть скидка 90% на каждый закэшированный токен. Запись в кэш стоит 1.25x — на 25% дороже, так как требуется сохранить KV-тензоры. Расширенное кэширование на один час стоит 2.0x.

Вот как это выглядит на моделях Claude от Anthropic:

![](https://miro.medium.com/v2/resize:fit:679/0*mcE2oZE665vak9Ir)

Эта экономика работает только при высоком cache hit-rate. Лучший продакшен-пример — Claude Code.

## 30-минутная сессия кодинга в Claude Code

Claude Code полностью построен вокруг одной цели — держать кэш «горячим».

Вот как выглядит реальная 30-минутная сессия с точки зрения биллинга.

Минута 0: Claude Code загружает системный промпт, определения инструментов и файл проекта CLAUDE.md. Этот payload превышает 20 000 токенов, и так как все токены новые, это самый дорогой момент всей сессии. Но эта стоимость оплачивается только один раз.

Минуты 1–5: вы начинаете давать инструкции, и Claude Code запускает Explore Subagent для обхода кодовой базы, открытия файлов и выполнения команд grep. Всё это добавляется в динамический суффикс. При этом статический префикс на 20 000 токенов теперь читается из кэша по $0.30 за миллион токенов вместо $3.00.

Минуты 6–15: Plan Subagent получает сжатый бриф вместо сырых результатов, так как передача сырого вывода раздула бы динамический суффикс. Он формирует план реализации, вы его подтверждаете, и Claude Code начинает вносить изменения. На каждом шаге статический префикс читается из кэша, hit-rate превышает 90%, а каждое обращение сбрасывает TTL, поддерживая кэш «горячим».

Минуты 16–25: вы запрашиваете изменения, что означает новые вызовы инструментов, больше вывода из терминала и рост контекста в динамическом суффиксе. К этому моменту сессия уже обработала сотни тысяч токенов, но на каждом шаге базовый префикс в 20 000 токенов читается из кэша.

## Get @vibecoding\_tg’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

Минута 28: вы запускаете `/cost` в терминале. Без кэширования 2 миллиона токенов по тарифу Sonnet 4.5 стоили бы $6.00. При эффективности кэша 92% — 1.84 миллиона токенов были прочитаны из кэша, и итоговая стоимость составила $1.15. Это снижение затрат на 81% для одной задачи.

![](https://miro.medium.com/v2/resize:fit:680/0*JFWiIdkExbkIf5oW)

Так выглядит «горячий» кэш. Статическую основу оплачиваете один раз, дальше она читается из кэша. Оплата идёт только за динамический хвост.

## Хрупкость кэширования на основе хэшей

Вот самый контринтуитивный момент в кэшировании промптов:

«1 + 2 = 3» работает, а «2 + 1» — уже cache miss.

Инфраструктура хэширует всю последовательность токенов с самого начала. Любое изменение в этой последовательности, даже просто перестановка двух элементов, меняет хэш, и весь префикс пересчитывается заново по полной цене.

![](https://miro.medium.com/v2/resize:fit:680/0*yASWZA5NS7on7F-X)

Это не второстепенная деталь реализации. Это ключевое ограничение, вокруг которого выстроены все инженерные решения в Claude Code.

Реальные примеры, которые ломали кэш в продакшене:

Таймстамп, добавляемый в системный промпт, создавал уникальный хэш на каждый запрос.

JSON-сериализатор, который по-разному сортировал ключи схемы инструментов между запросами, инвалидировал префикс.

AgentTool, параметры которого обновлялись в середине сессии, сбрасывал весь кэш на 20 000 токенов.

Из этого следуют три правила:

1/ Не изменять инструменты в рамках сессии. Определения инструментов входят в кэшируемый префикс, поэтому добавление или удаление инструмента инвалидирует всё, что идёт дальше.

2/ Не переключать модель в середине сессии. Кэш привязан к конкретной модели, поэтому переход на более дешёвую модель требует пересборки всего кэша с нуля.

3/ Не мутировать префикс для обновления состояния. Вместо редактирования системного промпта Claude Code добавляет reminder-тег к следующему пользовательскому сообщению, чтобы префикс оставался неизменным.

## Применение к собственным агентам

Те же правила работают как в Claude Code, так и при сборке агента с нуля.

Структурируйте промпты в следующем порядке:

Системные инструкции и поведенческие правила сверху. Не менять в ходе сессии.

Далее определения всех инструментов. Не добавлять и не удалять.

Затем извлечённый контекст и референсные документы. Держать стабильными на протяжении сессии.

Внизу история диалога и выводы инструментов. Это динамический суффикс.

![](https://miro.medium.com/v2/resize:fit:680/0*Qc5ES9v34tg-8qvw)

При включённом автокэшировании в API Anthropic граница кэша сдвигается автоматически по мере роста диалога. Без него пришлось бы вручную отслеживать границы токенов, и ошибка в границе означает полный промах по кэшу.

Для сжатия контекста при приближении к лимиту используйте cache-safe fork. Сохраняется тот же системный промпт, инструменты и история диалога, а инструкция на сжатие добавляется как новое сообщение. Кэшированный префикс переиспользуется, и тарифицируются только новые токены инструкции.

![](https://miro.medium.com/v2/resize:fit:680/0*597x8APO-F02UB79)

Чтобы проверить работу кэширования, отслеживайте три поля в каждом ответе API:

cache\_creation\_input\_tokens — токены, записанные в кэш.

cache\_read\_input\_tokens — токены, отданные из кэша.

input\_tokens — токены, обработанные без кэширования.

Эффективность кэша считается как

cache\_read\_input\_tokens / (cache\_read\_input\_tokens + cache\_creation\_input\_tokens).

Отслеживайте её так же, как отслеживаете аптайм.

## Ключевые выводы

Кэширование промптов — это не фича, которую просто включают. Это архитектурная дисциплина, вокруг которой нужно проектировать систему.

Базовая идея простая: статический контент размещается сверху, динамический растёт снизу. Инфраструктура хэширует префикс, сохраняет KV-тензоры и даёт ~90% экономии на каждом последующем чтении.

Сложность — в деталях. Не вставлять таймстампы в системные промпты, не менять порядок или состав инструментов, не переключать модель в середине сессии и не мутировать ничего выше границы кэша.

Claude Code показывает это на масштабе: 92% cache hit-rate и снижение стоимости на 81%. Если строить агентов без учёта кэширования промптов, теряется значительная часть маржи.

На этом всё.

Если этот разбор был полезен: вот мой телеграм канал — [https://t.me/+0WI99AjK6JRiNTc6](https://t.me/+0WI99AjK6JRiNTc6)

[Claude Code](https://medium.com/tag/claude-code?source=post_page-----4b47b76b8f10---------------------------------------)

[Vibe Coding](https://medium.com/tag/vibe-coding?source=post_page-----4b47b76b8f10---------------------------------------)

[AI](https://medium.com/tag/ai?source=post_page-----4b47b76b8f10---------------------------------------)

[AI Agent](https://medium.com/tag/ai-agent?source=post_page-----4b47b76b8f10---------------------------------------)

[Generative Ai Tools](https://medium.com/tag/generative-ai-tools?source=post_page-----4b47b76b8f10---------------------------------------)

2

2

[![@vibecoding_tg](https://miro.medium.com/v2/resize:fill:48:48/1*xw7X9UeF6LOT9hAIKjQiZA.jpeg)](https://medium.com/@vibecoding_tg?source=post_page---post_author_info--4b47b76b8f10---------------------------------------)

[![@vibecoding_tg](https://miro.medium.com/v2/resize:fill:64:64/1*xw7X9UeF6LOT9hAIKjQiZA.jpeg)](https://medium.com/@vibecoding_tg?source=post_page---post_author_info--4b47b76b8f10---------------------------------------)

Follow

[**Written by @vibecoding\_tg**](https://medium.com/@vibecoding_tg?source=post_page---post_author_info--4b47b76b8f10---------------------------------------)

[27 followers](https://medium.com/@vibecoding_tg/followers?source=post_page---post_author_info--4b47b76b8f10---------------------------------------)

· [1 following](https://medium.com/@vibecoding_tg/following?source=post_page---post_author_info--4b47b76b8f10---------------------------------------)

more posts - [https://t.me/+0WI99AjK6JRiNTc6](https://t.me/+0WI99AjK6JRiNTc6)

Follow

## No responses yet

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40vibecoding_tg%2F%25D0%25BA%25D1%258D%25D1%2588%25D0%25B8%25D1%2580%25D0%25BE%25D0%25B2%25D0%25B0%25D0%25BD%25D0%25B8%25D0%25B5-%25D0%25BF%25D1%2580%25D0%25BE%25D0%25BC%25D0%25BF%25D1%2582%25D0%25BE%25D0%25B2-%25D0%25B2-%25D0%25B1%25D0%25BE%25D0%25BB%25D1%258C%25D1%2588%25D0%25B8%25D1%2585-%25D1%258F%25D0%25B7%25D1%258B%25D0%25BA%25D0%25BE%25D0%25B2%25D1%258B%25D1%2585-%25D0%25BC%25D0%25BE%25D0%25B4%25D0%25B5%25D0%25BB%25D1%258F%25D1%2585-4b47b76b8f10&source=---post_responses--4b47b76b8f10---------------------respond_sidebar------------------)

Cancel

Respond

## More from @vibecoding\_tg

![Топ slash-команд и кастомных навыков в Claude Code](https://miro.medium.com/v2/resize:fit:679/format:webp/0*XCn3OWIfdrOQciaT)

[![@vibecoding_tg](https://miro.medium.com/v2/resize:fill:20:20/1*xw7X9UeF6LOT9hAIKjQiZA.jpeg)](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10----0---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[@vibecoding\_tg](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10----0---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[**Топ slash-команд и кастомных навыков в Claude Code**\\
\\
**Я прошёлся по официальной документации Claude Code, более чем 2300 комьюнити-навыкам и репозиторию awesome-claude-code, чтобы найти…**](https://medium.com/@vibecoding_tg/%D1%82%D0%BE%D0%BF-slash-%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4-%D0%B8-%D0%BA%D0%B0%D1%81%D1%82%D0%BE%D0%BC%D0%BD%D1%8B%D1%85-%D0%BD%D0%B0%D0%B2%D1%8B%D0%BA%D0%BE%D0%B2-%D0%B2-claude-code-03e806f3dfef?source=post_page---author_recirc--4b47b76b8f10----0---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

4d ago

[A clap icon3](https://medium.com/@vibecoding_tg/%D1%82%D0%BE%D0%BF-slash-%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4-%D0%B8-%D0%BA%D0%B0%D1%81%D1%82%D0%BE%D0%BC%D0%BD%D1%8B%D1%85-%D0%BD%D0%B0%D0%B2%D1%8B%D0%BA%D0%BE%D0%B2-%D0%B2-claude-code-03e806f3dfef?source=post_page---author_recirc--4b47b76b8f10----0---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

![Скиллы могут использовать сабагентов, сабагенты могут использовать скиллы.](https://miro.medium.com/v2/resize:fit:679/format:webp/0*ZxbHS_lXbTYlBw2K)

[![@vibecoding_tg](https://miro.medium.com/v2/resize:fill:20:20/1*xw7X9UeF6LOT9hAIKjQiZA.jpeg)](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10----1---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[@vibecoding\_tg](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10----1---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[**Скиллы могут использовать сабагентов, сабагенты могут использовать скиллы.**\\
\\
**Я начал использовать сабагентов в Claude Code, чтобы изолировать контекст от основной сессии.**](https://medium.com/@vibecoding_tg/%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B-%D0%BC%D0%BE%D0%B3%D1%83%D1%82-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D1%81%D0%B0%D0%B1%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2-%D1%81%D0%B0%D0%B1%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B-%D0%BC%D0%BE%D0%B3%D1%83%D1%82-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B-d379c8103ef7?source=post_page---author_recirc--4b47b76b8f10----1---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

Apr 7

[A clap icon3](https://medium.com/@vibecoding_tg/%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B-%D0%BC%D0%BE%D0%B3%D1%83%D1%82-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D1%81%D0%B0%D0%B1%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2-%D1%81%D0%B0%D0%B1%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B-%D0%BC%D0%BE%D0%B3%D1%83%D1%82-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B-d379c8103ef7?source=post_page---author_recirc--4b47b76b8f10----1---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

![Компоненты кодинг-агентов](https://miro.medium.com/v2/resize:fit:679/format:webp/0*PS_4grDM7IEuTkof.png)

[![@vibecoding_tg](https://miro.medium.com/v2/resize:fill:20:20/1*xw7X9UeF6LOT9hAIKjQiZA.jpeg)](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10----2---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[@vibecoding\_tg](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10----2---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[**Компоненты кодинг-агентов**\\
\\
**@vibecoding\_tg**](https://medium.com/@vibecoding_tg/%D0%BA%D0%BE%D0%BC%D0%BF%D0%BE%D0%BD%D0%B5%D0%BD%D1%82%D1%8B-%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2-2526b9aac866?source=post_page---author_recirc--4b47b76b8f10----2---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

Apr 5

[A clap icon1](https://medium.com/@vibecoding_tg/%D0%BA%D0%BE%D0%BC%D0%BF%D0%BE%D0%BD%D0%B5%D0%BD%D1%82%D1%8B-%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2-2526b9aac866?source=post_page---author_recirc--4b47b76b8f10----2---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

![Claude Managed Agents: как развернуть своего первого агента уже сегодня](https://miro.medium.com/v2/resize:fit:679/format:webp/c8790a6ac4cec21263a79305da5e27032b2811c3bb5ebcbf60bd0ade41026a5c)

[![@vibecoding_tg](https://miro.medium.com/v2/resize:fill:20:20/1*xw7X9UeF6LOT9hAIKjQiZA.jpeg)](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10----3---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[@vibecoding\_tg](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10----3---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[**Claude Managed Agents: как развернуть своего первого агента уже сегодня**\\
\\
**Статья будет обновляться по мере появления новой информации**](https://medium.com/@vibecoding_tg/claude-managed-agents-%D0%BA%D0%B0%D0%BA-%D1%80%D0%B0%D0%B7%D0%B2%D0%B5%D1%80%D0%BD%D1%83%D1%82%D1%8C-%D1%81%D0%B2%D0%BE%D0%B5%D0%B3%D0%BE-%D0%BF%D0%B5%D1%80%D0%B2%D0%BE%D0%B3%D0%BE-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%B0-%D1%83%D0%B6%D0%B5-%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F-cd72a2f776c6?source=post_page---author_recirc--4b47b76b8f10----3---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

Apr 9

[A clap icon1](https://medium.com/@vibecoding_tg/claude-managed-agents-%D0%BA%D0%B0%D0%BA-%D1%80%D0%B0%D0%B7%D0%B2%D0%B5%D1%80%D0%BD%D1%83%D1%82%D1%8C-%D1%81%D0%B2%D0%BE%D0%B5%D0%B3%D0%BE-%D0%BF%D0%B5%D1%80%D0%B2%D0%BE%D0%B3%D0%BE-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%B0-%D1%83%D0%B6%D0%B5-%D1%81%D0%B5%D0%B3%D0%BE%D0%B4%D0%BD%D1%8F-cd72a2f776c6?source=post_page---author_recirc--4b47b76b8f10----3---------------------83f89be4_f7b4_4e7d_85de_8886af28ecd2--------------)

[See all from @vibecoding\_tg](https://medium.com/@vibecoding_tg?source=post_page---author_recirc--4b47b76b8f10---------------------------------------)

## Recommended from Medium

![Google’s Gemma 4 Changes Everything for Open Source AI](https://miro.medium.com/v2/resize:fit:679/format:webp/1*gzdCtZq51MD8iMPX5YgyYA.png)

[![Towards Deep Learning](https://miro.medium.com/v2/resize:fill:20:20/1*LF1EF4T2UFrpxYubZ7r_7g.png)](https://medium.com/towards-deep-learning?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

In

[Towards Deep Learning](https://medium.com/towards-deep-learning?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

by

[Sumit Pandey](https://medium.com/@sumit.ai?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[**Google’s Gemma 4 Changes Everything for Open Source AI**\\
\\
**SameApache 2.0. Runs on your laptop. Beats models 20x its size. This is not a drill.**](https://medium.com/towards-deep-learning/googles-gemma-4-changes-everything-for-open-source-ai-ecd91934458f?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

Apr 3

[A clap icon1.3K\\
\\
A response icon24](https://medium.com/towards-deep-learning/googles-gemma-4-changes-everything-for-open-source-ai-ecd91934458f?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

![A quiet shift in power: Qwen’s open-source AI core emerges from the shadows, challenging the dominance of closed corporate models.](https://miro.medium.com/v2/resize:fit:679/format:webp/1*Xi5NxKh9VaV79bx6OyJ6dg.png)

[![Suleiman Tawil](https://miro.medium.com/v2/resize:fill:20:20/1*oej3hyYVseQigyP7zGqFAQ.png)](https://medium.com/@stawils?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[Suleiman Tawil](https://medium.com/@stawils?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[**Qwen Just Quietly Became the Most Dangerous Open-Source AI Model**\\
\\
**The most-downloaded AI model family on Earth was built by a small team with fewer resources than its competitors. Then Alibaba restructured…**](https://medium.com/@stawils/qwen-just-quietly-became-the-most-dangerous-open-source-ai-model-b5bcf7b2743c?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

Mar 31

[A clap icon1.8K\\
\\
A response icon49](https://medium.com/@stawils/qwen-just-quietly-became-the-most-dangerous-open-source-ai-model-b5bcf7b2743c?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

![Claude Code Ultraplan Launched: I Just Tested It (And It’s Better Than It Looks)](https://miro.medium.com/v2/resize:fit:679/format:webp/1*W5hbs5lyrNhL9Jzij7k4xg.png)

[![Joe Njenga](https://miro.medium.com/v2/resize:fill:20:20/1*0Hoc7r7_ybnOvk1t8yR3_A.jpeg)](https://medium.com/@joe.njenga?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[Joe Njenga](https://medium.com/@joe.njenga?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[**Claude Code Ultraplan Launched: I Just Tested It (And It’s Better Than It Looks)**\\
\\
**Anthropic has added Claude Code ultraplan, and I was quick to test it. You might like it or hate it for one reason — I’ll talk about that…**](https://medium.com/@joe.njenga/claude-code-ultraplan-launched-i-just-tested-it-and-its-better-than-it-looks-21a628332e97?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

Apr 4

[A clap icon902\\
\\
A response icon26](https://medium.com/@joe.njenga/claude-code-ultraplan-launched-i-just-tested-it-and-its-better-than-it-looks-21a628332e97?source=post_page---read_next_recirc--4b47b76b8f10----0---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

![If You Understand These 5 AI Terms, You’re Ahead of 90% of People](https://miro.medium.com/v2/resize:fit:679/format:webp/1*qbVrf-wO9PYtthAj6E4RYQ.png)

[![Towards AI](https://miro.medium.com/v2/resize:fill:20:20/1*JyIThO-cLjlChQLb6kSlVQ.png)](https://medium.com/towards-artificial-intelligence?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

In

[Towards AI](https://medium.com/towards-artificial-intelligence?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

by

[Shreyas Naphad](https://medium.com/@shreyasnaphad?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[**If You Understand These 5 AI Terms, You’re Ahead of 90% of People**\\
\\
**Master the core ideas behind AI without getting lost**](https://medium.com/towards-artificial-intelligence/if-you-understand-these-5-ai-terms-youre-ahead-of-90-of-people-c7622d353319?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

Mar 29

[A clap icon11K\\
\\
A response icon228](https://medium.com/towards-artificial-intelligence/if-you-understand-these-5-ai-terms-youre-ahead-of-90-of-people-c7622d353319?source=post_page---read_next_recirc--4b47b76b8f10----1---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

![Vibe Coding is Over illustration of three ai generated landing pages with the words IT’S OVER written at the top in large text](https://miro.medium.com/v2/resize:fit:679/format:webp/1*1OGKfKCooEZbKCSoSXXY8g.png)

[![Michal Malewicz](https://miro.medium.com/v2/resize:fill:20:20/1*149zXrb2FXvS_mctL4NKSg.png)](https://medium.com/@michalmalewicz?source=post_page---read_next_recirc--4b47b76b8f10----2---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[Michal Malewicz](https://medium.com/@michalmalewicz?source=post_page---read_next_recirc--4b47b76b8f10----2---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[**Vibe Coding is OVER.**\\
\\
**Here’s What Comes Next.**](https://medium.com/@michalmalewicz/vibe-coding-is-over-5a84da799e0d?source=post_page---read_next_recirc--4b47b76b8f10----2---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

Mar 24

[A clap icon6.1K\\
\\
A response icon235](https://medium.com/@michalmalewicz/vibe-coding-is-over-5a84da799e0d?source=post_page---read_next_recirc--4b47b76b8f10----2---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

![Building Claude Code with Harness Engineering](https://miro.medium.com/v2/resize:fit:679/format:webp/1*XIe0AzU8UNuX0Wqco7ouZg.png)

[![Level Up Coding](https://miro.medium.com/v2/resize:fill:20:20/1*5D9oYBd58pyjMkV_5-zXXQ.jpeg)](https://medium.com/gitconnected?source=post_page---read_next_recirc--4b47b76b8f10----3---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

In

[Level Up Coding](https://medium.com/gitconnected?source=post_page---read_next_recirc--4b47b76b8f10----3---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

by

[Fareed Khan](https://medium.com/@fareedkhandev?source=post_page---read_next_recirc--4b47b76b8f10----3---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[**Building Claude Code with Harness Engineering**\\
\\
**Multi-agents, MCP, skills system, context pipelines and more**](https://medium.com/gitconnected/building-claude-code-with-harness-engineering-d2e8c0da85f0?source=post_page---read_next_recirc--4b47b76b8f10----3---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

Apr 6

[A clap icon1.2K\\
\\
A response icon9](https://medium.com/gitconnected/building-claude-code-with-harness-engineering-d2e8c0da85f0?source=post_page---read_next_recirc--4b47b76b8f10----3---------------------b6a1b539_d1bd_41b8_b747_476907731882--------------)

[See more recommendations](https://medium.com/?source=post_page---read_next_recirc--4b47b76b8f10---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----4b47b76b8f10---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----4b47b76b8f10---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----4b47b76b8f10---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----4b47b76b8f10---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----4b47b76b8f10---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----4b47b76b8f10---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----4b47b76b8f10---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----4b47b76b8f10---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----4b47b76b8f10---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**