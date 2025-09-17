# 🎯 React Tender Agent with File Processing# LangGraph ReAct Agent Template



LangGraph-powered intelligent agent for tender analysis with advanced PDF and DOCX file processing capabilities.[![CI](https://github.com/langchain-ai/react-agent/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/react-agent/actions/workflows/unit-tests.yml)

[![Integration Tests](https://github.com/langchain-ai/react-agent/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/langchain-ai/react-agent/actions/workflows/integration-tests.yml)

## 🚀 Features[![Open in - LangGraph Studio](https://img.shields.io/badge/Open_in-LangGraph_Studio-00324d.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4NS4zMzMiIGhlaWdodD0iODUuMzMzIiB2ZXJzaW9uPSIxLjAiIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHBhdGggZD0iTTEzIDcuOGMtNi4zIDMuMS03LjEgNi4zLTYuOCAyNS43LjQgMjQuNi4zIDI0LjUgMjUuOSAyNC41QzU3LjUgNTggNTggNTcuNSA1OCAzMi4zIDU4IDcuMyA1Ni43IDYgMzIgNmMtMTIuOCAwLTE2LjEuMy0xOSAxLjhtMzcuNiAxNi42YzIuOCAyLjggMy40IDQuMiAzLjQgNy42cy0uNiA0LjgtMy40IDcuNkw0Ny4yIDQzSDE2LjhsLTMuNC0zLjRjLTQuOC00LjgtNC44LTEwLjQgMC0xNS4ybDMuNC0zLjRoMzAuNHoiLz48cGF0aCBkPSJNMTguOSAyNS42Yy0xLjEgMS4zLTEgMS43LjQgMi41LjkuNiAxLjcgMS44IDEuNyAyLjcgMCAxIC43IDIuOCAxLjYgNC4xIDEuNCAxLjkgMS40IDIuNS4zIDMuMi0xIC42LS42LjkgMS40LjkgMS41IDAgMi43LS41IDIuNy0xIDAtLjYgMS4xLS44IDIuNi0uNGwyLjYuNy0xLjgtMi45Yy01LjktOS4zLTkuNC0xMi4zLTExLjUtOS44TTM5IDI2YzAgMS4xLS45IDIuNS0yIDMuMi0yLjQgMS41LTIuNiAzLjQtLjUgNC4yLjguMyAyIDEuNyAyLjUgMy4xLjYgMS41IDEuNCAyLjMgMiAyIDEuNS0uOSAxLjItMy41LS40LTMuNS0yLjEgMC0yLjgtMi44LS44LTMuMyAxLjYtLjQgMS42LS41IDAtLjYtMS4xLS4xLTEuNS0uNi0xLjItMS42LjctMS43IDMuMy0yLjEgMy41LS41LjEuNS4yIDEuNi4zIDIuMiAwIC43LjkgMS40IDEuOSAxLjYgMi4xLjQgMi4zLTIuMy4yLTMuMi0uOC0uMy0yLTEuNy0yLjUtMy4xLTEuMS0zLTMtMy4zLTMtLjUiLz48L3N2Zz4=)](https://langgraph-studio.vercel.app/templates/open?githubUrl=https://github.com/langchain-ai/react-agent)



- **🔍 Tender Analysis**: Extracts key information from tender documentsThis template showcases a [ReAct agent](https://arxiv.org/abs/2210.03629) implemented using [LangGraph](https://github.com/langchain-ai/langgraph), designed for [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio). ReAct agents are uncomplicated, prototypical agents that can be flexibly extended to many tools.

- **📄 PDF Processing**: Full support for PDF file analysis

- **📝 DOCX Processing**: Word document processing and analysis  ![Graph view in LangGraph studio UI](./static/studio_ui.png)

- **🔢 Smart Calculations**: Budget analysis and deadline checking

- **🌐 Web Search**: Integration with Tavily for market researchThe core logic, defined in `src/react_agent/graph.py`, demonstrates a flexible ReAct agent that iteratively reasons about user queries and executes actions, showcasing the power of this approach for complex problem-solving tasks.

- **⏰ Time Management**: Deadline tracking and alerts

- **📊 Report Generation**: Formatted tender reports## What it does



## 🔧 Tools Available (19 total)The ReAct agent:



### Core Tools1. Takes a user **query** as input

1. `search` - Web search functionality2. Reasons about the query and decides on an action

2. `get_current_time` - Current time and date3. Executes the chosen action using available tools

3. `calculate` - Mathematical calculations4. Observes the result of the action

5. Repeats steps 2-4 until it can provide a final answer

### Tender Analysis

4. `extract_tender_info` - Extract tender detailsBy default, it's set up with a basic set of tools, but can be easily extended with custom tools to suit various use cases.

5. `format_tender_report` - Generate formatted reports

6. `check_tender_deadline` - Deadline validation## Getting Started



### File OperationsAssuming you have already [installed LangGraph Studio](https://github.com/langchain-ai/langgraph-studio?tab=readme-ov-file#download), to set up:

7. `read_file_content` - Read local files

8. `analyze_document` - Document analysis1. Create a `.env` file.

9. `list_files_in_directory` - Directory listing

```bash

### File Upload Processingcp .env.example .env

10. `process_uploaded_file` - Basic file upload handler```

11. `extract_text_from_content` - Text extraction

12. `handle_file_upload` - Universal file object handler2. Define required API keys in your `.env` file.

13. `analyze_uploaded_content` - Content analysis

14. `process_any_file_content` - Universal parameter handlerThe primary [search tool](./src/react_agent/tools.py) [^1] used is [Tavily](https://tavily.com/). Create an API key [here](https://app.tavily.com/sign-in).

15. `handle_file_content` - PDF file handler with logging

16. `handle_docx_content` - DOCX file handler### Setup Model

17. `universal_file_handler` - Auto-detecting file handler

18. `process_any_content_type` - Error-catching content processorThe defaults values for `model` are shown below:



### Debug Tools```yaml

19. `debug_input_data` - Development debuggingmodel: anthropic/claude-3-5-sonnet-20240620

```

## 📋 Supported File Types

Follow the instructions below to get set up, or pick one of the additional options.

- ✅ **PDF** (`application/pdf`)

- ✅ **DOCX** (`application/vnd.openxmlformats-officedocument.wordprocessingml.document`) #### Anthropic

- ✅ **Text files** (`text/plain`, `.txt`, `.md`, `.csv`)

- ✅ **JSON** (`application/json`)To use Anthropic's chat models:



## 🛠️ Quick Start1. Sign up for an [Anthropic API key](https://console.anthropic.com/) if you haven't already.

2. Once you have your API key, add it to your `.env` file:

### Local Development

```

1. **Clone and setup**:ANTHROPIC_API_KEY=your-api-key

```bash```

git clone <repository-url>#### OpenAI

cd react-tender-agent

pip install -e .To use OpenAI's chat models:

```

1. Sign up for an [OpenAI API key](https://platform.openai.com/signup).

2. **Configure environment**:2. Once you have your API key, add it to your `.env` file:

```bash```

cp .env.example .envOPENAI_API_KEY=your-api-key

# Add your API keys:```

# OPENAI_API_KEY=your_openai_key

# TAVILY_API_KEY=your_tavily_key  3. Customize whatever you'd like in the code.

# LANGSMITH_API_KEY=your_langsmith_key4. Open the folder LangGraph Studio!

```

## How to customize

3. **Run development server**:

```bash1. **Add new tools**: Extend the agent's capabilities by adding new tools in [tools.py](./src/react_agent/tools.py). These can be any Python functions that perform specific tasks.

langgraph dev --port 81282. **Select a different model**: We default to Anthropic's Claude 3 Sonnet. You can select a compatible chat model using `provider/model-name` via runtime context. Example: `openai/gpt-4-turbo-preview`.

```3. **Customize the prompt**: We provide a default system prompt in [prompts.py](./src/react_agent/prompts.py). You can easily update this via context in the studio.



4. **Open Studio**: You can also quickly extend this template by:

   - API: http://127.0.0.1:8128

   - Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8128- Modifying the agent's reasoning process in [graph.py](./src/react_agent/graph.py).

- Adjusting the ReAct loop or adding additional steps to the agent's decision-making process.

### LangGraph Cloud Deployment

## Development

This project is ready for deployment to LangGraph Platform:

While iterating on your graph, you can edit past state and rerun your app from past states to debug specific nodes. Local changes will be automatically applied via hot reload. Try adding an interrupt before the agent calls tools, updating the default system message in `src/react_agent/context.py` to take on a persona, or adding additional nodes and edges!

1. Create deployment in LangGraph Platform

2. Connect to this GitHub repository  Follow up requests will be appended to the same thread. You can create an entirely new thread, clearing previous history, using the `+` button in the top right.

3. Set environment variables in platform

4. Deploy automatically on pushYou can find the latest (under construction) docs on [LangGraph](https://github.com/langchain-ai/langgraph) here, including examples and other references. Using those guides can help you pick the right patterns to adapt here for your use case.



## 📊 Usage ExamplesLangGraph Studio also integrates with [LangSmith](https://smith.langchain.com/) for more in-depth tracing and collaboration with teammates.



### File Analysis[^1]: https://python.langchain.com/docs/concepts/#tools

```
"Проанализируй загруженный PDF файл"
"Обработай этот DOCX документ"
"Извлеки информацию о тендере из файла"
```

### Tender Operations
```
"Найди информацию о тендерах в энергетике"
"Проверь дедлайн тендера: 25.12.2025"
"Создай отчет по тендеру с бюджетом 1,000,000 рублей"
```

### Calculations
```
"Посчитай стоимость с НДС для суммы 850,000 рублей"
"Сколько дней до 31.12.2025?"
```

## 🔧 Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...              # OpenAI API key
TAVILY_API_KEY=tvly-...            # Tavily search API key

# Optional  
LANGSMITH_API_KEY=lsv2_pt_...      # LangSmith tracing
LANGCHAIN_TRACING_V2=true          # Enable tracing
LANGCHAIN_PROJECT=react-tender-agent
```

## 🎯 Architecture

- **Framework**: LangGraph with ReAct pattern
- **LLM**: OpenAI GPT-4o-mini with tool calling
- **Search**: Tavily API integration
- **File Processing**: PyPDF2, python-docx, lxml
- **Monitoring**: LangSmith tracing
- **Deployment**: LangGraph Platform ready

## 📝 Recent Updates

- ✅ Fixed PDF file processing (`application/pdf`)
- ✅ Fixed DOCX file processing (`application/vnd.openxmlformats-officedocument.wordprocessingml.document`)
- ✅ Added universal file handlers for different input formats
- ✅ Implemented error-catching and auto-recovery for unsupported content types
- ✅ Added comprehensive debugging tools for development
- ✅ Enhanced file upload capabilities for LangGraph Studio

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test file processing
langgraph dev --port 8128
# Upload PDF/DOCX files in Studio and test analysis
```

## 📄 License

Licensed under the MIT License. See `LICENSE` file for details.

---

**🚀 Ready for LangGraph Platform deployment with GitHub integration!**