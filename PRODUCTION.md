# React Tender Agent - Production Guide

## 🚀 Готов к развертыванию!

### ✅ Настроено:
- **OpenAI GPT-4o-mini** для основной логики
- **Tavily Search API** для веб-поиска
- **LangSmith** для трейсинга и мониторинга
- **LangGraph Platform Plus** план активирован
- **Wolfi Linux** для безопасности контейнера

### 🔧 Команды развертывания:

#### Локальная разработка:
```bash
# Запуск development сервера
langgraph dev --port 8126

# Доступ:
# API: http://127.0.0.1:8126
# Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8126
# Docs: http://127.0.0.1:8126/docs
```

#### Облачное развертывание:
```bash
# Развертывание в LangGraph Cloud
langgraph up

# Мониторинг статуса
langgraph status

# Получение логов
langgraph logs
```

### 🎯 Возможности агента:

1. **Веб-поиск**: Использует Tavily для поиска актуальной информации
2. **ReAct паттерн**: Рассуждение → Действие → Наблюдение
3. **Тендерная специализация**: Настроен для работы с тендерами и энергетикой
4. **Трейсинг**: Полная видимость в LangSmith

### 📋 API Examples:

#### Простой запрос:
```bash
curl -X POST "http://your-deployment-url/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {"messages": [{"role": "user", "content": "Найди информацию о тендерах в энергетике"}]},
    "stream_mode": "values"
  }'
```

### 🔐 Environment Variables:
- `OPENAI_API_KEY`: ✅ Настроен
- `TAVILY_API_KEY`: ✅ Настроен  
- `LANGSMITH_API_KEY`: ✅ Настроен
- `LANGCHAIN_TRACING_V2`: ✅ true

### 🏗️ Architecture:
```
User Input → ReAct Agent → Tavily Search → GPT-4o-mini → Response
                ↓
            LangSmith Tracing
```

### 🎪 Next Steps:
1. ✅ Local testing completed
2. 🔄 Cloud deployment in progress
3. 📈 Production monitoring ready
4. 🔧 Custom tools can be added to `src/react_agent/tools.py`