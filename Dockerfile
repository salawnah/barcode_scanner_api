FROM ubuntu:24.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive
# Set the virtual environment path
ENV VIRTUAL_ENV=/opt/venv
# Add venv to PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libzbar0 \
    && rm -rf /1var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Set the working directory
WORKDIR /app

# Copy requirements and install python dependencies into the venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]

