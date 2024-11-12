FROM python:3.11

# Create app directory
WORKDIR /app

# Install app dependencies
COPY app/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY app /app

CMD [ "python", "main.py" ]
