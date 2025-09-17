# 🔧 Руководство по модификации LangGraph агента

## 📊 Структура проекта

```
src/react_agent/
├── graph.py       # Основная логика графа (узлы, рёбра, маршрутизация)
├── tools.py       # Инструменты агента
├── state.py       # Состояние графа
├── context.py     # Контекст выполнения
└── utils.py       # Утилиты (загрузка моделей)
```

## 1️⃣ Добавление новых инструментов

### Простой инструмент:

```python
# В tools.py добавить:

async def get_current_time() -> str:
    """Получить текущее время."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def calculate(expression: str) -> str:
    """Выполнить математические вычисления."""
    try:
        # Осторожно с eval! В продакшене используйте safer-eval
        result = eval(expression)
        return f"Результат: {result}"
    except Exception as e:
        return f"Ошибка в вычислении: {e}"

# Добавить в список TOOLS:
TOOLS: List[Callable[..., Any]] = [
    search,
    get_current_time,
    calculate
]
```

### Инструмент с API:

```python
import httpx

async def get_weather(city: str) -> str:
    """Получить погоду для города."""
    # Пример с OpenWeatherMap API
    api_key = "your_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"Погода в {city}: {temp}°C, {desc}"
        else:
            return f"Не удалось получить погоду для {city}"
```

### Инструмент с базой данных:

```python
import sqlite3
from typing import List, Dict

async def query_database(sql: str) -> List[Dict]:
    """Выполнить SQL запрос к базе тендеров."""
    # Подключение к базе данных тендеров
    conn = sqlite3.connect("tenders.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    finally:
        conn.close()
```

## 2️⃣ Модификация графа

### Добавление нового узла:

```python
# В graph.py добавить новый узел

async def preprocessing_node(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Предобработка входящих сообщений."""
    last_message = state.messages[-1]
    
    # Например, проверяем содержание на спам
    if "спам" in last_message.content.lower():
        return {
            "messages": [AIMessage(content="Извините, не могу обработать этот запрос.")]
        }
    
    # Или добавляем контекст
    enhanced_content = f"Контекст: тендеры в энергетике. Запрос: {last_message.content}"
    state.messages[-1].content = enhanced_content
    
    return {"messages": state.messages}

# Добавить узел в граф:
builder.add_node("preprocessing", preprocessing_node)
builder.add_edge("__start__", "preprocessing")
builder.add_edge("preprocessing", "call_model")
```

### Добавление условной логики:

```python
def advanced_routing(state: State) -> Literal["tools", "database", "weather", "__end__"]:
    """Умная маршрутизация по типу запроса."""
    last_message = state.messages[-1]
    
    if not isinstance(last_message, AIMessage):
        return "__end__"
    
    if not last_message.tool_calls:
        return "__end__"
    
    # Проверяем какой инструмент вызывается
    tool_name = last_message.tool_calls[0]["name"]
    
    if tool_name == "query_database":
        return "database"
    elif tool_name == "get_weather":
        return "weather" 
    else:
        return "tools"

# Добавить специализированные узлы:
builder.add_node("database", ToolNode([query_database]))
builder.add_node("weather", ToolNode([get_weather]))

# Обновить маршрутизацию:
builder.add_conditional_edges("call_model", advanced_routing)
```

## 3️⃣ Расширение состояния

```python
# В state.py добавить новые поля:

from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ExtendedState(State):
    user_preferences: Optional[dict] = None
    session_context: Optional[dict] = None
    search_history: List[str] = field(default_factory=list)
    
    def add_search_term(self, term: str):
        """Добавить термин в историю поиска."""
        self.search_history.append(term)
        # Ограничить историю последними 10 запросами
        if len(self.search_history) > 10:
            self.search_history = self.search_history[-10:]
```

## 4️⃣ Workflow разработки

### Локальное тестирование:

```bash
# 1. Остановить текущий сервер
pkill -f langgraph

# 2. Внести изменения в код

# 3. Запустить dev сервер с hot-reload
cd /workspaces/react-tender-agent
.venv/bin/langgraph dev --port 8126

# 4. Тестировать в Studio:
# https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8126
```

### Production развертывание:

```bash
# 1. Тестирование production build локально
.venv/bin/langgraph up

# 2. Проверка в Studio:
# https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123

# 3. Развертывание в облако (после настройки credentials)
.venv/bin/langgraph deploy
```

## 5️⃣ Примеры полезных инструментов

### Анализ документов:

```python
import PyPDF2
from pathlib import Path

async def analyze_pdf(file_path: str) -> str:
    """Анализировать PDF документ тендера."""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Простой анализ ключевых слов
        keywords = ["цена", "срок", "требования", "условия"]
        found_info = {}
        
        for keyword in keywords:
            if keyword in text.lower():
                found_info[keyword] = "найдено"
        
        return f"Анализ PDF: {found_info}"
    except Exception as e:
        return f"Ошибка при анализе PDF: {e}"
```

### Уведомления:

```python
import smtplib
from email.mime.text import MIMEText

async def send_notification(message: str, email: str) -> str:
    """Отправить уведомление о новом тендере."""
    try:
        # Настройки SMTP (используйте переменные окружения!)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your_email@gmail.com"
        sender_password = "your_password"
        
        msg = MIMEText(message)
        msg['Subject'] = 'Новый тендер найден'
        msg['From'] = sender_email
        msg['To'] = email
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return "Уведомление отправлено"
    except Exception as e:
        return f"Ошибка отправки: {e}"
```

## 🔥 Pro Tips:

1. **Всегда тестируйте локально** перед production
2. **Используйте переменные окружения** для API ключей
3. **Добавляйте обработку ошибок** в каждый инструмент
4. **Логируйте действия** через LangSmith
5. **Версионируйте изменения** в git

## 🎯 Быстрый старт:

1. Откройте `src/react_agent/tools.py`
2. Добавьте новую функцию
3. Добавьте её в список `TOOLS`
4. Перезапустите `langgraph dev`
5. Тестируйте в Studio!