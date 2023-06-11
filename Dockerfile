FROM python3.8
RUN pip install --upgrade pip \
    #installing requirements.txt
    && pip install -r requirements.txt
# Copying the source code to Working Directory
COPY . /app
# Setting the Working Directory
WORKDIR /app
# Running the app
CMD ["python", "app.py"]
