FROM python:3.10

# Copy the requirements.txt file
COPY requirements.txt .

# Update with apt then install the python dependencies requirements.txt
RUN apt update && pip install -r requirements.txt

WORKDIR /app
