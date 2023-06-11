FROM python:3.8-slim
RUN pip install -r requirements.txt
# Copying the source code to Working Directory
COPY . /app
# Setting the Working Directory
WORKDIR /app
# Running the app
CMD ["python", "app.py"]
