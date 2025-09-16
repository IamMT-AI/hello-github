# Architecture Overview

This document describes the architecture of the AI Cartoon Figurine Generation MVP (Week 1).

## System Overview

The system is designed as a microservices architecture with the following key components:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │    │  Stylize2D       │    │  Fusion Service │
│   (FastAPI)     │───▶│  Service         │───▶│  (Library)      │
│   Port: 8000    │    │  Port: 8001      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   File Storage  │    │  Model Cache     │    │  3D Processing  │
│   (Local/Cloud) │    │  (SDXL + LoRA)   │    │  (Mesh Ops)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Components

### 1. API Gateway (`apps/api-gateway/`)

**Purpose**: Entry point for all client requests, handles routing and orchestration.

**Key Features**:
- File upload validation and processing
- Request routing to appropriate services
- Response aggregation and error handling
- Metrics collection and logging
- CORS and middleware management

**Endpoints**:
- `POST /api/upload` - Upload and process face image
- `GET /health` - Health check and service status
- `GET /` - Root endpoint with service info

### 2. 2D Stylization Service (`services/stylize2d/`)

**Purpose**: Converts uploaded face images to cartoon 2D style.

**Key Features**:
- Image validation and preprocessing
- SDXL + LoRA model inference (placeholder in MVP)
- Latency simulation and performance metrics
- Multiple output formats support

**Integration Points**:
- Called by API Gateway via HTTP
- Future: Model caching and GPU optimization
- Future: Queue system for batch processing

### 3. Fusion Service (`services/fusion/`)

**Purpose**: Combines stylized face with 3D body templates.

**Key Features**:
- Face-to-body mapping and alignment
- 3D geometry processing and mesh operations
- Quality scoring and validation
- Support for multiple body templates

**Usage**:
- Library-style integration (not a standalone service)
- Called directly by API Gateway
- Future: Separate service for scaling

### 4. Common Libraries (`libs/common/`)

**Purpose**: Shared utilities and cross-cutting concerns.

**Components**:
- **Logging**: Structured logging with Prometheus metrics placeholder
- **Metrics**: Request tracking and performance monitoring
- **Utilities**: Common helper functions and decorators

## Data Flow

### Image Processing Pipeline

1. **Upload** (`/api/upload`)
   ```
   Client → API Gateway → Validation → Stylization → Fusion → Response
   ```

2. **Stylization Process**
   ```
   Raw Image → Preprocessing → Model Inference → Post-processing → Stylized Image
   ```

3. **Fusion Process**
   ```
   Stylized Face + Body Template → Alignment → Mesh Operations → 3D Model
   ```

## Technology Stack

### Core Technologies
- **Python 3.9+**: Primary development language
- **FastAPI**: API framework for high performance
- **Uvicorn**: ASGI server for FastAPI applications
- **Pydantic**: Data validation and serialization
- **Structlog**: Structured logging

### Future Integrations (Post-MVP)
- **SDXL + LoRA**: 2D stylization model
- **ArcFace**: Face similarity evaluation
- **CLIP**: Style consistency evaluation
- **Trimesh**: 3D geometry processing
- **PyKDTree**: Spatial data structures
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards

## Deployment Architecture

### MVP Week 1 (Local Development)
```
localhost:8000 (API Gateway) → localhost:8001 (Stylize2D)
```

### Future Production Architecture
```
Load Balancer → API Gateway (Multi-instance)
                    ↓
GPU Cluster ← Stylization Service (Auto-scaling)
                    ↓
Message Queue ← Fusion Service (Multi-instance)
                    ↓
Object Storage ← File Management Service
```

## Configuration Management

### Environment Variables
- `STYLIZE_SERVICE_URL`: URL for 2D stylization service
- `MAX_FILE_SIZE`: Maximum upload file size
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `METRICS_ENABLED`: Enable/disable metrics collection

### Configuration Files
- `pyproject.toml`: Python project configuration
- `requirements.txt`: Python dependencies
- `Makefile`: Development and deployment commands

## Security Considerations

### MVP Week 1 (Simplified)
- Basic file validation (size, type, format)
- CORS configuration for development
- Input sanitization for uploaded files

### Future Security Features
- Authentication and authorization middleware
- Rate limiting and request throttling
- Input validation and sanitization
- Secure file storage with encryption
- API key management and rotation

## Monitoring and Observability

### Current Implementation
- Request timing middleware
- Structured logging with contextual information
- Basic health check endpoints
- Error tracking and reporting

### Future Monitoring
- Prometheus metrics collection
- Grafana dashboards for visualization
- Distributed tracing with OpenTelemetry
- Log aggregation and search
- Performance profiling and optimization

## Scalability Considerations

### Horizontal Scaling
- Stateless service design
- Load balancer compatibility
- Shared storage for file handling
- Database for order management

### Performance Optimization
- Model caching and preloading
- GPU utilization optimization
- Async processing for I/O operations
- Connection pooling for database access

## Error Handling

### Error Categories
1. **Client Errors (4xx)**: Invalid input, unsupported formats
2. **Server Errors (5xx)**: Service failures, model errors
3. **Timeout Errors**: Long-running operations
4. **Resource Errors**: Disk space, memory limits

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "File too large. Max size: 10MB",
    "details": {
      "file_size": 15728640,
      "max_size": 10485760
    },
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

## Future Architecture Evolution

### Phase 2: Model Integration
- Real SDXL + LoRA integration
- ArcFace and CLIP model deployment
- GPU optimization and model serving

### Phase 3: Production Scaling
- Kubernetes deployment
- Microservice separation
- Database integration for order management
- Cloud storage for files and models

### Phase 4: Advanced Features
- Real-time processing updates
- Batch processing capabilities
- Advanced 3D processing pipeline
- Print optimization and validation