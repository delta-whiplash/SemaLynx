FROM python:3.8-slim
# Copying the source code to Working Directory

COPY . /app
# Setting the Working Directory
WORKDIR /app

RUN pip install -r requirements.txt
# Running the app
CMD ["python", "app.py"]
