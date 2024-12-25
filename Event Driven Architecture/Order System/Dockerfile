FROM python:3.11.11-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
EXPOSE 8000
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . .

CMD ["fastapi", "run", "Order Service/main.py", "--port", "8000","--reload"]