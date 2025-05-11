# Global Alcohol Consumption Dashboard

This project is a Dash-based interactive dashboard for analyzing global alcohol consumption trends.

## Deployment with Docker

### Prerequisites
- Docker installed on your system
- Docker Compose (optional)

### Running the Application

1. Build the Docker image:
```bash
docker build -t vdi_project .
```

2. Run the container:
```bash
docker run -p 8050:8050 vdi_project
```

3. Access the dashboard:
Open your web browser and navigate to:
```
http://localhost:8050/
```

The dashboard will be available at this address and you can start exploring the global alcohol consumption data.
