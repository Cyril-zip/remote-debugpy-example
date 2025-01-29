# Use a smaller base image
FROM python:3.11.11-bullseye

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --upgrade debugpy && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy project files
COPY . /usr/src/app/

COPY ./app /usr/src/app/
COPY ./main.py /usr/src/app/
RUN mkdir /usr/src/app/debugpy_logs

EXPOSE 5000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1" ]