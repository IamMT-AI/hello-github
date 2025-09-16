# AI Cartoon Figurine Generation - MVP Week 1

> Transform your photos into personalized 3D cartoon figurines with AI-powered stylization and automated 3D model generation.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/IamMT-AI/hello-github.git
cd hello-github

# Set up development environment
make setup

# Start the API Gateway
make run-api
```

The API Gateway will start on `http://localhost:8000`.

### Starting Individual Services

```bash
# Terminal 1: API Gateway
make run-api

# Terminal 2: 2D Stylization Service
make run-stylize

# Terminal 3: Test the fusion service
make run-fusion
```

## 📖 API Usage

### Upload and Process Image

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@your_face_image.jpg"
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🏗️ Architecture

This MVP implements a microservices architecture with the following components:

- **API Gateway** (`apps/api-gateway/`) - Request routing and orchestration
- **2D Stylization Service** (`services/stylize2d/`) - AI-powered image stylization
- **Fusion Service** (`services/fusion/`) - Face-to-body 3D model integration
- **Common Libraries** (`libs/common/`) - Shared utilities and logging

## 📁 Project Structure

```
.
├── README.md
├── LICENSE (MIT)
├── CODEOWNERS
├── Makefile
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── docker/
│   └── Dockerfile.base
├── .github/workflows/ci.yml
├── apps/
│   └── api-gateway/
│       ├── main.py
│       └── routers/
│           └── upload.py
├── services/
│   ├── stylize2d/
│   │   └── server.py
│   └── fusion/
│       └── fuse.py
├── libs/
│   └── common/
│       ├── __init__.py
│       └── logging.py
├── models/
│   └── base/
│       └── README.md
├── scripts/
│   └── generate_test_orders.py
├── tools/
│   └── eval_avatar.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── latency-baseline-w1.md
│   └── print-test-report-w1.md
└── infra/
    └── observability/
        └── grafana-dashboard.json
```

## 🛠️ Development

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Run tests (when available)
make test
```

### Docker

```bash
# Build base Docker image
make docker-build

# Run with Docker
docker run -p 8000:8000 hello-github-mvp:base
```

## 🧪 Testing

### Generate Test Data

```bash
# Generate synthetic test orders
python scripts/generate_test_orders.py --count 100 --output test_orders.json

# Run avatar evaluation
python tools/eval_avatar.py \
  --original test_face.jpg \
  --avatar generated_avatar.png \
  --output evaluation.json
```

## 📊 Performance

### MVP Week 1 Baseline
- **End-to-End Latency**: < 3 seconds (placeholder services)
- **95th Percentile**: < 2 seconds for 512x512 images
- **Error Rate**: < 1% for valid inputs
- **Availability**: > 99% uptime target

See [docs/latency-baseline-w1.md](docs/latency-baseline-w1.md) for detailed performance metrics.

## 🔧 Configuration

### Environment Variables

- `STYLIZE_SERVICE_URL`: URL for 2D stylization service (default: http://localhost:8001)
- `MAX_FILE_SIZE`: Maximum upload file size (default: 10MB)
- `LOG_LEVEL`: Logging level (default: INFO)

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - System design and component details
- [Performance Baseline](docs/latency-baseline-w1.md) - MVP Week 1 performance metrics
- [Model Templates](models/base/README.md) - 3D body templates and model information

## 🚧 MVP Week 1 Status

This is the initial MVP Week 1 release focusing on:

- ✅ **Repository Structure**: Complete monorepo scaffolding
- ✅ **API Gateway**: Upload endpoint with validation
- ✅ **2D Stylization**: Placeholder service with latency simulation  
- ✅ **Fusion Service**: Basic face-body integration stub
- ✅ **Observability**: Logging and metrics placeholders
- ✅ **CI/CD**: GitHub Actions workflow
- ✅ **Docker**: Base container configuration

### Upcoming Features (Post-MVP)

- 🔄 **Real Model Integration**: SDXL + LoRA for 2D stylization
- 🔄 **3D Processing**: Advanced mesh operations with trimesh
- 🔄 **Quality Evaluation**: ArcFace + CLIP integration
- 🔄 **Authentication**: User management and API security
- 🔄 **Production Deployment**: Kubernetes and cloud infrastructure

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and run tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings for functions and classes
- Update documentation for significant changes
- Run `make format` and `make lint` before committing

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/IamMT-AI/hello-github/issues)
- 📖 **Documentation**: [docs/](docs/) directory
- 🔧 **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Structlog for structured logging
- The open-source community for inspiration and tools

---

**MVP Week 1** - Initial monorepo structure and service scaffolding
**Next Milestone**: Model integration and real AI pipeline implementation
