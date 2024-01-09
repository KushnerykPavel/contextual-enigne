# Use a Python base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Copy the entire project to the container
COPY . /app/

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Expose any necessary ports
# EXPOSE 8000
RUN mkdir /app/models

# Set the default command to run when the container starts
CMD [ "python", "main.py" ]