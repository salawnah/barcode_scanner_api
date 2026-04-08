# Barcode & QR Code Scanner API

An automated, containerized API built with FastAPI and `pyzbar` to decode barcodes and QR codes from uploaded images.
Note: This project is built using the gemma-4-26b-a4b GenAI model with the help of Continue (All copyrighted to their owners)

## 🚀 Features

* **FastAPI-powered**: High-performance asynchronous implementation.
* **Multi-format detection**: Supports various barcode formats (EAN13, Code128, etc.) and QR Codes.
* **Containerized**: Ready to deploy with Docker using an Ubuntu 24.04 base image.
* **Secure**: Protected by API Key authentication via the `X-API-Key` header.
* **Configurable**: Easily change the API key via environment variables.

## 🛠️ Prerequisites
* [Docker](https://www.docker.com/) installed on your machine.

## 🚀 Quick Start (Pre-built Image)
You can pull and run the pre-built Docker image directly from GitHub Container Registry:
```bash
docker run -d \
  --name barcode-api-container \
  -p 8000:8000 \
  -e SCANNER_API_KEY="your-secret-key-here" \
  ghcr.io/salawnah/barcode_scanner_api:main
```

## 📦 Setup & Building (Local Development)
Navigate to the project directory and build the Docker image:
```bash
cd barcode_scanner_api
docker build -t barcode-scanner-api .
```

## 🏃 Running the API

Run the container by mapping port `8000` and providing your desired API Key using the `SCANNER_API_KEY` environment variable:

```bash
docker run -d \
  --name barcode-api-container \
  -p 8000:8000 \
  -e SCANNER_API_KEY="your-secret-key-here" \
  barcode-scanner-api
```

## 🧪 Testing the API

Once the container is running, you can test it using `curl`. Replace `your-secret-key-here` with the key you used in the run command.

### 1. Test with correct API Key

```bash
curl -X 'POST' \
  'http://localhost:8000/scan' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -H 'X-API-Key: your-secret-key-here' \
  -F 'file=@path/to/your/barcode_image.png'
```

### 2. Test with incorrect API Key (Should return 403 Forbidden)

```bash
curl -I -X 'POST' \
  'http://localhost:8000/scan' \
  -H 'X-API-Key: wrong-key'
```

## 📂 Project Structure

* `main.py`: The core FastAPI application.
* `Dockerfile`: Instructions for building the Ubuntu 24.04 container.
* `requirements.txt`: Python dependencies (`fastapi`, `uvicorn`, `pyzbar`, etc.).
* `.gitignore`: Configured to keep your repository clean of junk files.