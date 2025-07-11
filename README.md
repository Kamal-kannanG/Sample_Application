# FastAPI File/Text Upload API

This project is a FastAPI REST application that exposes an endpoint for uploading text or files (PDF, DOCX, MD), extracts the text content, and returns it in a JSON response. It is container-ready for Azure Container Apps deployment and includes a GitHub Actions workflow for CI/CD.

## Features
- **/upload** endpoint:
  - Accepts either plain text (form or JSON) or a file upload (PDF, DOCX, MD).
  - Extracts and returns the text content from the uploaded file (file takes priority if both are provided).
- **/health** endpoint for health checks.
- Dockerfile for containerization.
- GitHub Actions workflow for automated build and deployment to Azure Container Apps.

## Local Development

1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn[standard] python-docx pymupdf python-multipart
   ```
2. **Run the app:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
3. **Test endpoints:**
   - Health check: [http://localhost:8000/health](http://localhost:8000/health)
   - API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Docker Usage

1. **Build the Docker image:**
   ```bash
   docker build -t fastapi-upload-app .
   ```
2. **Run the container:**
   ```bash
   docker run -p 8000:8000 fastapi-upload-app
   ```

## Azure Container Apps Deployment

1. **Update Dockerfile** to include all dependencies (including `python-multipart`).
2. **Build and push** the Docker image to Azure Container Registry (ACR).
3. **Deploy** to Azure Container Apps using the provided GitHub Actions workflow (`.github/workflows/azure-containerapps.yml`).

## GitHub Actions Workflow
- The workflow builds and pushes the Docker image to ACR and deploys it to Azure Container Apps on every push to the `main` branch.
- Set the following secrets in your repository:
  - `AZURE_CREDENTIALS`
  - `ACR_USERNAME`
  - `ACR_PASSWORD`

## API Example

### Upload File (PDF/DOCX/MD)
```
curl -X POST "http://localhost:8000/upload" -F "file=@yourfile.pdf"
```

### Upload Text
```
curl -X POST "http://localhost:8000/upload" -F "text=Hello world!"
```

### JSON Text
```
curl -X POST "http://localhost:8000/upload" -H "Content-Type: application/json" -d '{"text": "Hello world!"}'
```

## License
MIT
