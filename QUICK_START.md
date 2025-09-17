# 🚀 Быстрый старт: Изменение и тестирование агента

## ✅ Что вы уже добавили:

### 🔧 Новые инструменты в `tools.py`:
1. **`get_current_time()`** - получение текущего времени
2. **`calculate(expression)`** - математические вычисления
3. **`extract_tender_info(text)`** - извлечение информации о тендерах
4. **`format_tender_report()`** - форматирование отчетов

## 🏃‍♂️ Workflow разработки

### 1️⃣ Внести изменения:
```bash
# Редактировать файлы в VS Code:
# - src/react_agent/tools.py (новые инструменты)
# - src/react_agent/graph.py (логика графа)
```

### 2️⃣ Тестировать локально:
```bash
# Остановить текущий сервер
pkill -f "langgraph dev"

# Запустить dev сервер с изменениями
cd /workspaces/react-tender-agent
.venv/bin/langgraph dev --port 8127

# Открыть Studio для тестирования
# https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8127
```

### 3️⃣ Тестировать через API:
```bash
# Тест новых инструментов
curl -X POST "http://127.0.0.1:8127/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {"messages": [{"role": "user", "content": "Какое время? Вычисли 100*5+20"}]},
    "stream_mode": "values"
  }'

# Тест анализа тендера
curl -X POST "http://127.0.0.1:8127/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {"messages": [{"role": "user", "content": "Анализируй этот текст тендера: Заказчик ПАО ЛУКОЙЛ. Поставка оборудования на сумму 5000000 рублей до 15.12.2025"}]},
    "stream_mode": "values"
  }'
```

### 4️⃣ Развернуть в production:
```bash
# Обновить production сервер
.venv/bin/langgraph up

# Проверить в production Studio
# https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
```

## 🎯 Примеры тестирования в Studio

### В чате Studio попробуйте:

#### ✨ Новые возможности:
- "Какое сейчас время?"
- "Вычисли 150 * 12 + 500"
- "Создай отчет по тендеру: 'Поставка энергооборудования', бюджет '2 млн руб', срок '30.12.2025', описание 'Закупка трансформаторов'"

#### 🔍 Анализ тендеров:
- "Проанализируй: Заказчик Россети. Модернизация подстанции 110кВ. Стоимость 15 млн рублей. Срок подачи заявок до 20.11.2025"

#### 🌐 Поиск + анализ:
- "Найди информацию о тендерах на поставку электрооборудования и создай отчет"

## 🛠️ Добавление собственных инструментов

### Шаблон нового инструмента:
```python
# В src/react_agent/tools.py добавить:

async def my_custom_tool(param1: str, param2: int) -> str:
    """Описание инструмента для агента."""
    try:
        # Ваша логика здесь
        result = f"Обработка {param1} с параметром {param2}"
        return result
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Добавить в список TOOLS:
TOOLS: List[Callable[..., Any]] = [
    search,
    get_current_time,
    calculate,
    extract_tender_info,
    format_tender_report,
    my_custom_tool  # ← Ваш новый инструмент
]
```

## 📊 Мониторинг

### LangSmith трейсинг:
- Все вызовы автоматически логируются
- Просматривайте трейсы на [smith.langchain.com](https://smith.langchain.com)
- Проект: `react-tender-agent`

### Логи сервера:
```bash
# Просмотр логов в реальном времени
tail -f ~/.langchain/logs/langgraph.log

# Или в терминале где запущен сервер
```

## 🎉 Готово!

Теперь у вас есть:
✅ **5 рабочих инструментов** (поиск + 4 новых)  
✅ **Development workflow** с hot-reload  
✅ **Production deployment** готов  
✅ **LangSmith трейсинг** настроен  
✅ **Документация** для команды  

### 🔄 Следующие шаги:
1. Тестируйте новые функции в Studio
2. Добавляйте специфичные для вашей области инструменты
3. Настраивайте промпты в `context.py`
4. Расширяйте граф в `graph.py`

**Happy coding! 🚀**