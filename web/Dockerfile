FROM python:3.10.6-slim

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt \
    && rm -rf requirements.txt

COPY . /app

EXPOSE 80

CMD ["streamlit", "run", "app.py", "--logger.level=debug"]