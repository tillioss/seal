# Deployment Guide

This guide covers development setup, testing, and deployment instructions for the SEAL API service.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for containerized deployment)
- Git
- A Gemini API key

### Local Development

1. **Clone and Setup**:

   ```bash
   git clone https://github.com/yourusername/seal.git
   cd seal
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   Create a `.env` file in the project root:

   ```env
   GOOGLE_API_KEY=your_api_key_here
   LLM_PROVIDER=gemini
   ```

3. **Run Development Server**:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **API Documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Test streaming endpoint: `curl -N -X POST http://localhost:8000/stream -H "Content-Type: application/json" -d '{"scores":{"EMT1":[35,40,38]}, "metadata":{"class_id":"A1","deficient_area":"EMT1","num_students":25}}'`

### Code Style and Quality

- Use [black](https://github.com/psf/black) for code formatting
- Use [flake8](https://flake8.pycqa.org/) for linting
- Use [mypy](http://mypy-lang.org/) for type checking

```bash
pip install black flake8 mypy
black .
flake8 .
mypy .
```

## Docker Deployment

### Local Docker Build

1. **Build the Image**:

   ```bash
   docker build -t seal-api .
   ```

2. **Run with Docker**:
   ```bash
   docker run -p 8000:8000 \
     -e GOOGLE_API_KEY=your_api_key_here \
     seal-api
   ```

### Docker Compose

1. **Start the Service**:

   ```bash
   docker compose up -d
   ```

2. **View Logs**:

   ```bash
   docker compose logs -f
   ```

3. **Stop the Service**:
   ```bash
   docker compose down
   ```

## Production Deployment

### Security Considerations

1. **API Key Management**:

   - Never commit API keys to version control
   - Use environment variables or secrets management
   - Rotate keys regularly

2. **CORS Configuration**:

   - Update CORS settings in `main.py` for production
   - Specify exact allowed origins
   - Remove wildcard permissions

3. **Rate Limiting**:
   - Implement rate limiting for API endpoints
   - Consider using FastAPI's built-in middleware

### Deployment Options

1. **Cloud Run (Google Cloud)**:

   ```bash
   # Build the container
   docker build -t gcr.io/[PROJECT-ID]/seal-api .

   # Push to Container Registry
   docker push gcr.io/[PROJECT-ID]/seal-api

   # Deploy to Cloud Run
   gcloud run deploy seal-api \
     --image gcr.io/[PROJECT-ID]/seal-api \
     --platform managed \
     --allow-unauthenticated
   ```

2. **Kubernetes**:
   ```bash
   # Apply Kubernetes manifests
   kubectl apply -f k8s/
   ```

### Monitoring and Logging

1. **Application Logs**:

   - JSON-formatted logs for better parsing
   - Structured logging with context
   - Error tracking with stack traces

2. **Metrics**:

   - Response times
   - Error rates
   - Request counts
   - LLM latency

3. **Health Checks**:
   - `/health` endpoint for service health
   - LLM availability monitoring
   - Resource usage tracking

### Scaling Considerations

1. **Horizontal Scaling**:

   - Stateless application design
   - Load balancer configuration
   - Session handling (if needed)

2. **Resource Management**:

   - CPU and memory limits
   - Concurrent request handling
   - Connection pooling

3. **Cost Optimization**:
   - LLM API usage monitoring
   - Resource scaling policies
   - Caching strategies

## Troubleshooting

### Common Issues

1. **API Key Issues**:

   - Check environment variables
   - Verify API key permissions
   - Check for rate limiting

2. **Performance Issues**:

   - Monitor LLM response times
   - Check resource utilization
   - Review concurrent requests

3. **Docker Issues**:
   - Check container logs
   - Verify environment variables
   - Check network connectivity

### Support

For issues and support:

1. Check the [GitHub Issues](https://github.com/yourusername/seal/issues)
2. Review error logs
3. Contact the development team
