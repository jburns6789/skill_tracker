FROM python:3.9
RUN pip install fastapi uvicorn
COPY . /skilltree-api
WORKDIR /skilltree-api
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
