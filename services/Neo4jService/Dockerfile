# Dockerfile

# pull the official docker image
FROM python:3.9-slim

# VENV
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set work directory
WORKDIR /app

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
CMD ["python", "main.py"]