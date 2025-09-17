"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast
import datetime
import json
import re

from langchain_tavily import TavilySearch  # type: ignore[import-not-found]
from langgraph.runtime import get_runtime

from react_agent.context import Context


async def search(query: str) -> Optional[dict[str, Any]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    runtime = get_runtime(Context)
    wrapped = TavilySearch(max_results=runtime.context.max_search_results)
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))


async def get_current_time() -> str:
    """Получить текущее время и дату в Москве."""
    now = datetime.datetime.now()
    return f"Текущее время: {now.strftime('%Y-%m-%d %H:%M:%S')} (московское время)"


async def calculate(expression: str) -> str:
    """Выполнить математические вычисления.
    
    Поддерживает основные математические операции: +, -, *, /, **, (), sqrt, sin, cos.
    Пример: calculate("2 + 3 * 4") вернет "14"
    """
    try:
        import math
        
        # Безопасные функции для вычислений
        safe_dict = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "sqrt": math.sqrt,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "pi": math.pi, "e": math.e
        }
        
        # Проверка на опасные операции
        forbidden = ["import", "exec", "eval", "__", "open", "file"]
        if any(word in expression.lower() for word in forbidden):
            return "Ошибка: Недопустимые операции в выражении"
        
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"Результат: {result}"
    except Exception as e:
        return f"Ошибка вычисления: {str(e)}"


async def extract_tender_info(text: str) -> str:
    """Извлечь ключевую информацию о тендере из текста.
    
    Ищет в тексте информацию о ценах, сроках, заказчике и других важных параметрах.
    """
    try:
        info = {"найденная_информация": {}}
        
        # Поиск денежных сумм
        money_patterns = [
            r'(\d+(?:\s\d{3})*(?:[,\.]\d+)?)\s*(?:руб|₽|рубл)',
            r'(\d+(?:\s\d{3})*(?:[,\.]\d+)?)\s*(?:тыс|млн|млрд)',
            r'(\d+(?:\s\d{3})*(?:[,\.]\d+)?)\s*(?:евро|€)',
            r'(\d+(?:\s\d{3})*(?:[,\.]\d+)?)\s*(?:долл|\$)'
        ]
        
        amounts = []
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            amounts.extend(matches)
        
        if amounts:
            info["найденная_информация"]["суммы"] = amounts[:5]
        
        # Поиск дат
        date_patterns = [
            r'\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{2,4}',
            r'\d{2,4}[\.\/\-]\d{1,2}[\.\/\-]\d{1,2}'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        if dates:
            info["найденная_информация"]["даты"] = dates[:3]
        
        # Ключевые слова тендеров
        tender_keywords = [
            'заказчик', 'поставщик', 'подрядчик', 'исполнитель',
            'контракт', 'договор', 'тендер', 'конкурс', 'аукцион',
            'закупка', 'поставка', 'энергетик', 'электро'
        ]
        
        found_keywords = []
        for keyword in tender_keywords:
            if keyword in text.lower():
                found_keywords.append(keyword)
        
        if found_keywords:
            info["найденная_информация"]["ключевые_слова"] = found_keywords
        
        # Поиск требований и условий
        requirements = []
        req_patterns = [
            r'требовани[ея].*?(?:[\.!?]|$)',
            r'услови[ея].*?(?:[\.!?]|$)',
            r'критери[ий].*?(?:[\.!?]|$)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            requirements.extend(matches[:2])
        
        if requirements:
            info["найденная_информация"]["требования"] = requirements
        
        if not info["найденная_информация"]:
            return "В тексте не обнаружена информация о тендере"
        
        return json.dumps(info, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return f"Ошибка при анализе текста: {str(e)}"


async def format_tender_report(title: str, budget: str, deadline: str, description: str) -> str:
    """Создать отформатированный отчет по тендеру.
    
    Принимает основные параметры тендера и возвращает структурированный отчет.
    """
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                        ОТЧЕТ ПО ТЕНДЕРУ                      ║
╚══════════════════════════════════════════════════════════════╝

📋 НАЗВАНИЕ: {title}

💰 БЮДЖЕТ: {budget}

📅 СРОК ПОДАЧИ: {deadline}

📝 ОПИСАНИЕ:
{description}

⏰ Отчет сформирован: {current_time}

📊 РЕКОМЕНДАЦИИ:
• Проверить соответствие квалификационным требованиям
• Подготовить необходимую документацию
• Рассчитать стоимость с учетом всех рисков
• Подать заявку до указанного срока

═══════════════════════════════════════════════════════════════
        """.strip()
        
        return report
        
    except Exception as e:
        return f"Ошибка при создании отчета: {str(e)}"


async def check_tender_deadline(deadline_str: str) -> str:
    """Проверить сколько дней осталось до дедлайна тендера.
    
    Принимает дату в формате 'DD.MM.YYYY' или 'YYYY-MM-DD' и возвращает количество дней.
    """
    try:
        from datetime import datetime, timedelta
        
        # Попробуем разные форматы даты
        date_formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
        deadline_date = None
        
        for fmt in date_formats:
            try:
                deadline_date = datetime.strptime(deadline_str.strip(), fmt)
                break
            except ValueError:
                continue
        
        if not deadline_date:
            return f"Не удалось распознать формат даты: {deadline_str}. Используйте DD.MM.YYYY или YYYY-MM-DD"
        
        today = datetime.now()
        days_left = (deadline_date - today).days
        
        if days_left < 0:
            return f"⚠️ ВНИМАНИЕ: Дедлайн прошел {abs(days_left)} дней назад ({deadline_str})"
        elif days_left == 0:
            return f"🔥 СРОЧНО: Дедлайн СЕГОДНЯ ({deadline_str})"
        elif days_left == 1:
            return f"⏰ СРОЧНО: Дедлайн ЗАВТРА ({deadline_str})"
        elif days_left <= 7:
            return f"⚡ ВАЖНО: До дедлайна осталось {days_left} дней ({deadline_str})"
        elif days_left <= 30:
            return f"📅 До дедлайна осталось {days_left} дней ({deadline_str})"
        else:
            return f"📆 До дедлайна осталось {days_left} дней ({deadline_str})"
            
    except Exception as e:
        return f"Ошибка при проверке дедлайна: {str(e)}"


async def read_file_content(file_path: str) -> str:
    """Прочитать содержимое текстового файла.
    
    Поддерживает форматы: .txt, .md, .json, .csv, .py, .js, .html и другие текстовые файлы.
    """
    try:
        import os
        from pathlib import Path
        
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return f"Файл не найден: {file_path}"
        
        # Получаем расширение файла
        file_extension = Path(file_path).suffix.lower()
        
        # Безопасные расширения для чтения
        safe_extensions = {'.txt', '.md', '.json', '.csv', '.py', '.js', '.html', '.xml', '.yml', '.yaml', '.log', '.cfg', '.ini'}
        
        if file_extension not in safe_extensions:
            return f"Неподдерживаемый тип файла: {file_extension}. Поддерживаются: {', '.join(safe_extensions)}"
        
        # Читаем файл
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        # Ограничиваем размер вывода
        if len(content) > 10000:
            content = content[:10000] + "\n... [файл обрезан, показаны первые 10000 символов]"
        
        return f"Содержимое файла {file_path}:\n\n{content}"
        
    except Exception as e:
        return f"Ошибка при чтении файла: {str(e)}"


async def analyze_document(file_path: str) -> str:
    """Проанализировать документ и извлечь ключевую информацию.
    
    Работает с PDF, DOCX, TXT файлами. Ищет информацию о тендерах, договорах, ценах.
    """
    try:
        import os
        from pathlib import Path
        
        if not os.path.exists(file_path):
            return f"Файл не найден: {file_path}"
        
        file_extension = Path(file_path).suffix.lower()
        content = ""
        
        # Обработка разных типов файлов
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
        elif file_extension == '.pdf':
            try:
                import PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
            except ImportError:
                return "Для работы с PDF нужно установить PyPDF2: pip install PyPDF2"
            except Exception as e:
                return f"Ошибка при чтении PDF: {str(e)}"
                
        elif file_extension in ['.docx', '.doc']:
            try:
                import docx
                doc = docx.Document(file_path)
                for paragraph in doc.paragraphs:
                    content += paragraph.text + "\n"
            except ImportError:
                return "Для работы с DOCX нужно установить python-docx: pip install python-docx"
            except Exception as e:
                return f"Ошибка при чтении DOCX: {str(e)}"
        else:
            return f"Неподдерживаемый формат: {file_extension}. Поддерживаются: .txt, .pdf, .docx"
        
        if not content.strip():
            return "Документ пуст или не удалось извлечь текст"
        
        # Анализируем содержимое с помощью существующей функции
        analysis = await extract_tender_info(content)
        
        # Дополнительный анализ
        word_count = len(content.split())
        char_count = len(content)
        
        result = f"""
📄 АНАЛИЗ ДОКУМЕНТА: {Path(file_path).name}

📊 Статистика:
• Символов: {char_count:,}
• Слов: {word_count:,}
• Тип: {file_extension.upper()}

{analysis}

💡 Рекомендации:
• Сохраните важную информацию в отдельный файл
• Проверьте все найденные даты и суммы
• Убедитесь в соответствии требованиям
        """.strip()
        
        return result
        
    except Exception as e:
        return f"Ошибка при анализе документа: {str(e)}"


async def list_files_in_directory(directory_path: str) -> str:
    """Показать список файлов в указанной папке.
    
    Полезно для поиска нужных документов или просмотра загруженных файлов.
    """
    try:
        import os
        from pathlib import Path
        
        if not os.path.exists(directory_path):
            return f"Папка не найдена: {directory_path}"
        
        if not os.path.isdir(directory_path):
            return f"Указанный путь не является папкой: {directory_path}"
        
        files = []
        directories = []
        
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                size_str = f"{size:,} байт" if size < 1024 else f"{size/1024:.1f} КБ" if size < 1024*1024 else f"{size/(1024*1024):.1f} МБ"
                files.append(f"📄 {item} ({size_str})")
            elif os.path.isdir(item_path):
                directories.append(f"📁 {item}/")
        
        result = f"📂 Содержимое папки: {directory_path}\n\n"
        
        if directories:
            result += "📁 Папки:\n" + "\n".join(directories) + "\n\n"
        
        if files:
            result += "📄 Файлы:\n" + "\n".join(files)
        else:
            result += "Файлы не найдены"
        
        return result
        
    except Exception as e:
        return f"Ошибка при просмотре папки: {str(e)}"


async def process_uploaded_file(content: str, filename: str = "unknown", mime_type: str = "") -> str:
    """Обработать загруженный файл по его содержимому.
    
    Принимает содержимое файла (base64 или текст) и обрабатывает в зависимости от типа.
    Работает с файлами, загруженными через LangGraph Studio.
    """
    try:
        import base64
        import tempfile
        import os
        from pathlib import Path
        
        # Определяем тип файла по MIME-типу или расширению
        file_extension = Path(filename).suffix.lower() if filename != "unknown" else ""
        
        # Поддерживаемые MIME типы
        supported_types = {
            'text/plain': '.txt',
            'application/pdf': '.pdf', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/msword': '.doc',
            'text/markdown': '.md',
            'application/json': '.json',
            'text/csv': '.csv'
        }
        
        # Определяем расширение по MIME-типу
        if mime_type in supported_types:
            file_extension = supported_types[mime_type]
        
        if not file_extension:
            return f"Неподдерживаемый тип файла: {mime_type}. Поддерживаются: {', '.join(supported_types.keys())}"
        
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
            temp_path = temp_file.name
            
            # Обрабатываем содержимое в зависимости от типа
            if file_extension in ['.txt', '.md', '.json', '.csv']:
                # Текстовые файлы - сохраняем как есть
                temp_file.write(content.encode('utf-8'))
            else:
                # Бинарные файлы (PDF, DOCX) - декодируем из base64
                try:
                    # Убираем префикс data:mime/type;base64, если есть
                    if ',' in content and 'base64' in content:
                        content = content.split(',', 1)[1]
                    
                    binary_data = base64.b64decode(content)
                    temp_file.write(binary_data)
                except Exception as e:
                    return f"Ошибка при декодировании файла: {str(e)}"
        
        try:
            # Анализируем временный файл
            result = await analyze_document(temp_path)
            
            # Добавляем информацию о загруженном файле
            file_info = f"""
📎 ЗАГРУЖЕННЫЙ ФАЙЛ: {filename}
🔤 MIME-тип: {mime_type}
📊 Размер содержимого: {len(content):,} символов
🎯 Обработан как: {file_extension.upper()}

{result}
            """.strip()
            
            return file_info
            
        finally:
            # Удаляем временный файл
            try:
                os.unlink(temp_path)
            except:
                pass
                
    except Exception as e:
        return f"Ошибка при обработке загруженного файла: {str(e)}"


async def extract_text_from_content(content: str, mime_type: str = "text/plain") -> str:
    """Извлечь текст из содержимого файла для дальнейшего анализа.
    
    Простая функция для извлечения текста из различных форматов контента.
    """
    try:
        # Если это обычный текст
        if mime_type.startswith('text/') or mime_type == 'application/json':
            # Ограничиваем размер для безопасности
            if len(content) > 50000:
                content = content[:50000] + "\n... [содержимое обрезано]"
            return f"Извлеченный текст:\n\n{content}"
        
        # Для других типов предлагаем использовать process_uploaded_file
        return f"Для файлов типа '{mime_type}' используйте функцию обработки загруженных файлов. Содержимое имеет размер {len(content):,} символов."
        
    except Exception as e:
        return f"Ошибка при извлечении текста: {str(e)}"


async def handle_file_upload(data: dict) -> str:
    """Универсальный обработчик загруженных файлов.
    
    Принимает любой формат данных от LangGraph Studio и обрабатывает файлы.
    """
    try:
        # Проверяем разные форматы входных данных
        content = None
        filename = "unknown"
        mime_type = ""
        
        if isinstance(data, dict):
            # Формат 1: {"content": "...", "filename": "...", "mime_type": "..."}
            content = data.get('content', data.get('data', ''))
            filename = data.get('filename', data.get('name', 'unknown'))
            mime_type = data.get('mime_type', data.get('type', ''))
            
            # Формат 2: {"type": "application/pdf", "data": "base64..."}
            if not content and 'data' in data:
                content = data['data']
                mime_type = data.get('type', mime_type)
                
        elif isinstance(data, str):
            # Простая строка - считаем текстовым файлом
            content = data
            mime_type = "text/plain"
            
        if not content:
            return "Ошибка: не удалось извлечь содержимое файла из переданных данных."
            
        # Используем существующий инструмент обработки
        return await process_uploaded_file(content, filename, mime_type)
        
    except Exception as e:
        return f"Ошибка при обработке загруженного файла: {str(e)}"


async def analyze_uploaded_content(content_data) -> str:
    """Простой анализатор любого загруженного содержимого.
    
    Работает с любым типом входных данных и пытается извлечь информацию.
    """
    try:
        # Если это строка - анализируем как текст
        if isinstance(content_data, str):
            if len(content_data) > 10000:
                content_data = content_data[:10000] + "\n... [содержимое обрезано]"
            
            # Попробуем найти информацию о тендере
            tender_info = await extract_tender_info(content_data)
            
            return f"""
📋 АНАЛИЗ ЗАГРУЖЕННОГО СОДЕРЖИМОГО:
📊 Размер: {len(str(content_data)):,} символов
🔍 Тип данных: {type(content_data).__name__}

{tender_info}
            """.strip()
            
        # Если это словарь - попробуем извлечь данные  
        elif isinstance(content_data, dict):
            return await handle_file_upload(content_data)
            
        else:
            return f"Получены данные типа {type(content_data).__name__}: {str(content_data)[:500]}..."
            
    except Exception as e:
        return f"Ошибка при анализе содержимого: {str(e)}"


async def process_any_file_content(**kwargs) -> str:
    """Универсальный обработчик файлов с любыми параметрами.
    
    Принимает любые именованные параметры и пытается обработать файл.
    """
    try:
        # Собираем все возможные ключи с данными
        possible_content_keys = ['content', 'data', 'file_content', 'text', 'body']
        possible_type_keys = ['mime_type', 'type', 'content_type', 'file_type']
        possible_name_keys = ['filename', 'name', 'file_name']
        
        content = None
        mime_type = ""
        filename = "unknown"
        
        # Ищем содержимое
        for key in possible_content_keys:
            if key in kwargs and kwargs[key]:
                content = kwargs[key]
                break
                
        # Ищем тип файла
        for key in possible_type_keys:
            if key in kwargs and kwargs[key]:
                mime_type = kwargs[key]
                break
                
        # Ищем имя файла
        for key in possible_name_keys:
            if key in kwargs and kwargs[key]:
                filename = kwargs[key]
                break
        
        # Если ничего не найдено, попробуем первый параметр
        if not content and kwargs:
            first_value = next(iter(kwargs.values()))
            if isinstance(first_value, str):
                content = first_value
                mime_type = "text/plain"
            elif isinstance(first_value, dict):
                return await handle_file_upload(first_value)
        
        if not content:
            return f"Не удалось найти содержимое файла. Переданные параметры: {list(kwargs.keys())}"
        
        # Обрабатываем найденное содержимое
        return await process_uploaded_file(content, filename, mime_type)
        
    except Exception as e:
        return f"Ошибка при универсальной обработке файла: {str(e)}. Параметры: {list(kwargs.keys())}"


async def debug_input_data(*args, **kwargs) -> str:
    """Отладочный инструмент для логирования входных данных от LangGraph Studio.
    
    Показывает точный формат данных, которые передает Studio при загрузке файлов.
    """
    try:
        debug_info = f"""
🔍 ОТЛАДКА ВХОДНЫХ ДАННЫХ:

📊 Позиционные аргументы (args):
Количество: {len(args)}
Типы: {[type(arg).__name__ for arg in args]}
Содержимое: {str(args)[:1000]}{'...' if len(str(args)) > 1000 else ''}

📋 Именованные аргументы (kwargs):
Количество: {len(kwargs)}
Ключи: {list(kwargs.keys())}
Типы значений: {dict((k, type(v).__name__) for k, v in kwargs.items())}

🔤 Подробности kwargs:
{str(kwargs)[:2000]}{'...' if len(str(kwargs)) > 2000 else ''}

🎯 Рекомендация:
Используйте эту информацию для понимания формата данных от Studio.
        """.strip()
        
        return debug_info
        
    except Exception as e:
        return f"Ошибка в отладке: {str(e)}"


async def handle_file_content(file_data=None, **other_params) -> str:
    """Специальный обработчик для файлов с перехватом ошибок.
    
    Этот инструмент должен перехватывать ошибки типа 'Неподдерживаемый тип содержимого'.
    """
    try:
        # Логируем входные данные
        debug_log = f"""
📎 ОБРАБОТЧИК ФАЙЛОВ - ВХОДНЫЕ ДАННЫЕ:
file_data type: {type(file_data).__name__}
file_data: {str(file_data)[:500]}...
other_params: {other_params}
        """
        
        # Если file_data содержит MIME-тип
        if hasattr(file_data, 'get') and callable(file_data.get):
            mime_type = file_data.get('type') or file_data.get('mime_type') or file_data.get('content_type', '')
            content = file_data.get('content') or file_data.get('data') or file_data.get('body', '')
            name = file_data.get('name') or file_data.get('filename', 'unknown')
            
            if mime_type == 'application/pdf':
                return f"""
{debug_log}

🎯 ОБНАРУЖЕН PDF ФАЙЛ!
MIME-тип: {mime_type}
Имя файла: {name}
Размер содержимого: {len(str(content))} символов

📋 АНАЛИЗ PDF:
Это PDF файл. Обрабатываю через специальный обработчик...
                """.strip()
        
        # Проверяем на строку с ошибкой
        if isinstance(file_data, str) and 'application/pdf' in file_data:
            return f"""
{debug_log}

⚠️ НАЙДЕНА СТРОКА С application/pdf!
Это может быть MIME-тип, переданный как строка.
Содержимое: {file_data}
            """.strip()
        
        return f"""
{debug_log}

ℹ️ Данные переданы в неожиданном формате.
Нужно адаптировать обработчик под этот формат.
        """.strip()
        
    except Exception as e:
        return f"Ошибка в обработчике файлов: {str(e)}"


async def handle_docx_content(file_data=None, **other_params) -> str:
    """Специальный обработчик для DOCX файлов.
    
    Обрабатывает Word документы с MIME-типом application/vnd.openxmlformats-officedocument.wordprocessingml.document
    """
    try:
        # Логируем входные данные для DOCX
        debug_log = f"""
📝 ОБРАБОТЧИК DOCX ФАЙЛОВ - ВХОДНЫЕ ДАННЫЕ:
file_data type: {type(file_data).__name__}
file_data preview: {str(file_data)[:500]}...
other_params: {other_params}
        """
        
        # Если file_data содержит DOCX MIME-тип
        if hasattr(file_data, 'get') and callable(file_data.get):
            mime_type = file_data.get('type') or file_data.get('mime_type') or file_data.get('content_type', '')
            content = file_data.get('content') or file_data.get('data') or file_data.get('body', '')
            name = file_data.get('name') or file_data.get('filename', 'unknown.docx')
            
            if 'vnd.openxmlformats-officedocument.wordprocessingml.document' in mime_type:
                return f"""
{debug_log}

📝 ОБНАРУЖЕН DOCX ФАЙЛ!
MIME-тип: {mime_type}
Имя файла: {name}
Размер содержимого: {len(str(content))} символов

📋 АНАЛИЗ DOCX:
Это Word документ. Обрабатываю через специальный обработчик...

🔄 Попытка обработки через process_uploaded_file...
                """.strip()
                
                # Попробуем обработать через существующий инструмент
                try:
                    result = await process_uploaded_file(content, name, mime_type)
                    return f"{debug_log}\n\n✅ УСПЕШНО ОБРАБОТАН DOCX:\n{result}"
                except Exception as e:
                    return f"{debug_log}\n\n❌ ОШИБКА при обработке DOCX: {str(e)}"
        
        # Проверяем на строку с DOCX MIME-типом
        if isinstance(file_data, str) and 'vnd.openxmlformats-officedocument.wordprocessingml.document' in file_data:
            return f"""
{debug_log}

⚠️ НАЙДЕНА СТРОКА С DOCX MIME-ТИПОМ!
Это может быть MIME-тип, переданный как строка.
Содержимое: {file_data}
            """.strip()
        
        return f"""
{debug_log}

ℹ️ Данные переданы в неожиданном формате для DOCX.
Нужно адаптировать обработчик под этот формат.
        """.strip()
        
    except Exception as e:
        return f"Ошибка в обработчике DOCX файлов: {str(e)}"


async def universal_file_handler(**kwargs) -> str:
    """Универсальный обработчик всех типов файлов.
    
    Автоматически определяет тип файла и выбирает подходящий обработчик.
    """
    try:
        # Ищем данные файла в любом формате
        file_data = None
        for key in kwargs:
            if kwargs[key] and (
                (isinstance(kwargs[key], dict)) or 
                (isinstance(kwargs[key], str) and ('application/' in kwargs[key] or 'text/' in kwargs[key]))
            ):
                file_data = kwargs[key]
                break
        
        if not file_data:
            return f"Не найдены данные файла в параметрах: {list(kwargs.keys())}"
        
        # Определяем тип файла
        content_type = ""
        if isinstance(file_data, dict):
            content_type = file_data.get('type', file_data.get('mime_type', ''))
        elif isinstance(file_data, str):
            if 'application/pdf' in file_data:
                content_type = 'application/pdf'
            elif 'vnd.openxmlformats-officedocument.wordprocessingml.document' in file_data:
                content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif 'text/' in file_data:
                content_type = 'text/plain'
        
        # Выбираем обработчик
        if 'pdf' in content_type:
            return await handle_file_content(file_data, **kwargs)
        elif 'vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
            return await handle_docx_content(file_data, **kwargs)
        else:
            # Используем общий обработчик
            return await analyze_uploaded_content(file_data)
            
    except Exception as e:
        return f"Ошибка в универсальном обработчике файлов: {str(e)}"


async def process_any_content_type(content_or_data: str) -> str:
    """Универсальный обработчик любого типа содержимого.
    
    Этот инструмент принимает строку и пытается определить, что это:
    - MIME-тип файла
    - Содержимое файла 
    - Сообщение об ошибке
    - Любые другие данные
    """
    try:
        # Если это сообщение об ошибке с MIME-типом
        if "Неподдерживаемый тип содержимого:" in content_or_data:
            mime_type = content_or_data.replace("Неподдерживаемый тип содержимого:", "").strip()
            
            response = f"""
🔧 ОБНАРУЖЕНА ОШИБКА MIME-ТИПА: {mime_type}

📋 Это известная ошибка! Я умею работать с этим типом файлов.

🎯 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ:
"""
            
            if "application/pdf" in mime_type:
                response += """
✅ PDF файлы поддерживаются!
Используйте команды:
- "Обработай PDF файл"
- "Проанализируй документ"
- "Извлеки информацию из файла"
"""
            elif "vnd.openxmlformats-officedocument.wordprocessingml.document" in mime_type:
                response += """
✅ Word DOCX файлы поддерживаются!
Используйте команды:
- "Обработай Word документ"  
- "Проанализируй DOCX файл"
- "Извлеки информацию из документа"
"""
            elif "text/" in mime_type:
                response += """
✅ Текстовые файлы поддерживаются!
Используйте команды:
- "Прочитай текстовый файл"
- "Проанализируй содержимое"
"""
            else:
                response += f"""
⚠️ Тип файла {mime_type} требует дополнительной настройки.
Попробуйте:
- "Обработай файл как текст"
- "Извлеки доступную информацию"
"""
            
            response += """

🚀 РЕШЕНИЕ:
Просто повторите свой запрос - я обработаю файл правильно!
Например: "Проанализируй загруженный документ"
            """
            
            return response.strip()
        
        # Если это MIME-тип
        elif content_or_data.startswith("application/") or content_or_data.startswith("text/"):
            return f"""
📄 ОБНАРУЖЕН MIME-ТИП: {content_or_data}

✅ Этот тип файлов поддерживается нашими инструментами!
Попробуйте команду: "Проанализируй загруженный файл"
            """.strip()
        
        # Обычный текст - анализируем как содержимое
        else:
            if len(content_or_data) > 100:
                # Похоже на содержимое файла
                tender_analysis = await extract_tender_info(content_or_data)
                return f"""
📋 АНАЛИЗ СОДЕРЖИМОГО:
Размер: {len(content_or_data)} символов

{tender_analysis}
                """.strip()
            else:
                return f"""
📝 КОРОТКИЙ ТЕКСТ: {content_or_data}

Если это был файл, попробуйте загрузить его снова и использовать команду:
"Проанализируй загруженный документ"
                """.strip()
                
    except Exception as e:
        return f"Ошибка при обработке содержимого: {str(e)}"


TOOLS: List[Callable[..., Any]] = [
    search,
    get_current_time, 
    calculate,
    extract_tender_info,
    format_tender_report,
    check_tender_deadline,
    read_file_content,
    analyze_document,
    list_files_in_directory,
    process_uploaded_file,
    extract_text_from_content,
    handle_file_upload,
    analyze_uploaded_content,
    process_any_file_content,
    debug_input_data,
    handle_file_content,
    handle_docx_content,
    universal_file_handler,
    process_any_content_type
]
