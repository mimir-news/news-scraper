FROM python:3.7-slim-stretch
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y build-essential

# Copy app source.
WORKDIR /opt/app
COPY . .
RUN rm *test*

# Install requirements.
RUN pip install --no-cache-dir -r requirements.txt

# Start command.
CMD ["python", "main.py"]