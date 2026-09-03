FROM python:3.11.9

# не создавать .pyc файлы (чистота)
ENV PYTHONDONTWRITEBYTECODE=1

# логи выводятся сразу, а не буферизируются (удобно для отладки)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]