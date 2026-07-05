# DevOps / SRE — Учебник

Учебный сайт по трекеру обучения DevOps/SRE: 5 фаз, 18 разделов, 215 тем, 190 вопросов в тестах. Весь сайт — один самодостаточный `index.html` (работает офлайн и на GitHub Pages).

## Структура

- `index.html` — готовый сайт (открыть в браузере или задеплоить на GitHub Pages)
- `data/topics.json` — темы, извлечённые из Google-таблицы трекера
- `data/section_*.json` — контент разделов (объяснения + тесты)
- `build.py` — собирает `data/*.json` в `index.html`
- `repair.py` — чинит типовые ошибки JSON после генерации контента

## Пересборка

```bash
python build.py
```

## Деплой на GitHub Pages

Достаточно закоммитить `index.html` в репозиторий и включить Pages (Settings → Pages → Deploy from branch). Прогресс чтения и результаты тестов хранятся в localStorage браузера.
