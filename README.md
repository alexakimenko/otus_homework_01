# Log Analyzer

Этот проект представляет собой анализатор логов, который помогает выявить URL'ы, вызывающие наибольшую задержку в веб-интерфейсе. Логи анализируются, и на их основе генерируется отчет в формате HTML, который включает статистику по URL'ам с наибольшим временем обработки.

## Функциональные возможности

- Обработка последнего (по дате) лога в директории.
- Поддержка логов как в сжатом (`.gz`), так и в несжатом формате.
- Генерация отчета в формате HTML с указанием наиболее "тяжелых" URL'ов.
- Поддержка конфигурации через файл, с возможностью переопределения настроек по умолчанию.
- Структурированное логирование с использованием `structlog`.

## Установка

Для установки всех необходимых зависимостей используется Poetry:

```bash
poetry install
```

### Использование

Запуск анализатора логов с указанием директории логов и отчета:

```bash
poetry run python src/app/log_analyzer.py --config config.yaml
```

### Пример конфигурации config.yaml

```yaml
log_dir: './logs'
report_dir: './reports'
report_size: 10
tablesorter_js: './jquery.tablesorter.min.js'
report_template: './report.html'
log_file: 'log_analyzer.log'
```

### Запуск тестов
Для запуска тестов с использованием pytest:

```bash
poetry run pytest --cov=src tests/
```

### CI/CD

Проект настроен на автоматическую проверку кода и запуск тестов с использованием GitHub Actions. Проверки включают:

	•	Линтер (flake8)
	•	Форматирование кода (black)
	•	Сортировку импортов (isort)
	•	Статическую проверку типов (mypy)
	•	Запуск тестов (pytest)
