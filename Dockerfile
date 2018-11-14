FROM python:3.7-slim-stretch
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    build-essential \
    python-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng12-dev

# Copy app source.
WORKDIR /opt/app
COPY . .
RUN rm *test*
RUN rm -rf tests

# Install requirements.
RUN pip install --no-cache-dir -r requirements.txt
RUN python download_newspaper_corpora.py

# Start command.
CMD ["python", "main.py"]